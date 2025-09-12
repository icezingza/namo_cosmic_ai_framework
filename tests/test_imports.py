import importlib.util
import pytest

@pytest.mark.parametrize("mod", ["core_modules", "api_integration"])
def test_packages_exist(mod):
    assert importlib.util.find_spec(mod) is not None, f"Missing package: {mod}"
