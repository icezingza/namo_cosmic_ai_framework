from sanitized_core import ANICCA_INIT, KARUNA_ROUTER, UPEKKHA_THROTTLE, INTENT_GATE

def test_init_profile():
    p = ANICCA_INIT("NaMo++")
    assert p["identity"] == "NaMo++"
    assert "teach" in p["modes"]

def test_router_compassion():
    plan = KARUNA_ROUTER({"intent":"teach"})
    assert plan["route"] == "compassion_first"
    assert plan["verdict"]["verdict"] == "allow"

def test_intent_gate_denies_exploit():
    v = INTENT_GATE({"intent":"test","bypass":True})
    assert v["verdict"] == "deny"

def test_throttle_bounds():
    q = UPEKKHA_THROTTLE(quality_target=0.9)
    assert q["status"] == "steady"
