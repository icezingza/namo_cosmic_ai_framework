from core.safety_system import SafetySystem


def test_safety_system_flags_prohibited_content():
    safety = SafetySystem()
    assert not safety.validate("This describes malware deployment")
    report = safety.report()
    assert report["content"] == 1
