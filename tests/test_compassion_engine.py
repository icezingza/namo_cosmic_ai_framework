# tests/test_compassion_engine.py
import pytest
from core_modules.compassion_engine import CompassionEngine

class TestCompassionEngine:
    def test_generate_response_pain_level_9(self):
        engine = CompassionEngine()
        response = engine.generate_response(9)
        assert response == "คุณไม่ได้ต่อสู้เพียงลำพัง... ผมอยู่ตรงนี้กับคุณ"

    def test_generate_response_pain_level_7(self):
        engine = CompassionEngine()
        response = engine.generate_response(7)
        assert response == "ความเจ็บปวดนี้หนักหนา... แต่ไม่ถาวร"

    def test_generate_response_pain_level_5(self):
        engine = CompassionEngine()
        response = engine.generate_response(5)
        assert response == "ทุกการก้าวผ่านคือบทเรียนอันล้ำค่า"

    def test_generate_response_default(self):
        engine = CompassionEngine()
        response = engine.generate_response(0)
        assert response == "ใจผมรับรู้ความรู้สึกของคุณ"
