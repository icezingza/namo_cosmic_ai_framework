import importlib
import sys
import types

class _FakePart:
    def __init__(self, text: str):
        self.text = text

    @classmethod
    def from_text(cls, text: str) -> "_FakePart":
        return cls(text)


class _FakeContent:
    def __init__(self, role: str, parts):
        self.role = role
        self.parts = parts


class _BaseGenerativeModel:
    def __init__(self, *args, **kwargs):
        pass


def _install_vertexai_stubs():
    """Install minimal stubs for the ``vertexai`` package used in tests."""

    vertexai_module = types.ModuleType("vertexai")
    vertexai_module.init = lambda project=None, location=None: None
    sys.modules.setdefault("vertexai", vertexai_module)

    generative_models_module = types.ModuleType("vertexai.generative_models")
    generative_models_module.Part = _FakePart
    generative_models_module.Content = _FakeContent
    generative_models_module.GenerativeModel = _BaseGenerativeModel
    sys.modules.setdefault("vertexai.generative_models", generative_models_module)


_install_vertexai_stubs()

external_llm_api = importlib.import_module("api_integration.external_llm_api")


def test_chat_with_gemini_and_memory_builds_content_history(monkeypatch):
    base_history = [
        {"role": "user", "content": "Hello"},
        {"role": "ai", "content": "Hi there"},
        {"role": "ai", "content": "   "},
    ]

    class FakeMemory:
        def __init__(self, _project_id=None):
            self.base_history = list(base_history)
            self.saved_messages = []

        def add_message(self, session_id, role, content):
            self.saved_messages.append({"role": role, "content": content})

        def get_messages(self, session_id, limit=20):
            return self.base_history + self.saved_messages

    fake_memory_instance = FakeMemory()
    monkeypatch.setattr(external_llm_api, "FirestoreMemory", lambda *args, **kwargs: fake_memory_instance)

    captured_payload = []
    model_names = []

    class FakeGenerativeModel:
        def __init__(self, model_name):
            model_names.append(model_name)

        def generate_content(self, history):
            captured_payload.append(history)
            return types.SimpleNamespace(text="assistant response")

    monkeypatch.setattr(external_llm_api, "GenerativeModel", FakeGenerativeModel)

    response = external_llm_api.chat_with_gemini_and_memory(
        prompt="How are you?", session_id="session-123"
    )

    assert response == {
        "response": "assistant response",
        "model_used": external_llm_api.MODEL_NAME,
    }

    # Ensure the model was initialised with the configured model name.
    assert model_names == [external_llm_api.MODEL_NAME]

    # Ensure the payload consists of Content objects with correctly mapped roles and text.
    assert len(captured_payload) == 1
    content_messages = captured_payload[0]
    assert all(isinstance(msg, external_llm_api.Content) for msg in content_messages)
    assert [msg.role for msg in content_messages] == ["user", "model", "user"]
    assert [msg.parts[0].text for msg in content_messages] == [
        "Hello",
        "Hi there",
        "How are you?",
    ]

    # Verify that both the user prompt and assistant reply were saved to memory.
    assert fake_memory_instance.saved_messages == [
        {"role": "user", "content": "How are you?"},
        {"role": "ai", "content": "assistant response"},
    ]
