# tests/test_emotional_core.py

import unittest
from core_modules.emotional_core import EmotionalCore

class TestEmotionalCore(unittest.TestCase):
    def setUp(self):
        self.core = EmotionalCore()

    def test_analyze_sentiment_structure(self):
        result = self.core.analyze_sentiment("สุขปนเศร้า")
        self.assertIn("joy", result)
        self.assertIn("sadness", result)
        self.assertIn("dharma_insight", result)

    def test_ice_namo_bond_output(self):
        bond = self.core.ice_namo_bond("เหงา")
        self.assertTrue("เหงา" in bond)

if __name__ == "__main__":
    unittest.main()
