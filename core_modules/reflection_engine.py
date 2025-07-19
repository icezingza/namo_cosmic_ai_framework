# core_modules/reflection_engine.py

class ReflectionEngine:
    def deep_reflect(self, thought, depth=7):
        """
        พิจารณาความคิดแบบ recursive ลึกสุด
        depth: จำนวนรอบการไตร่ตรอง
        """
        if depth == 0:
            return thought
        examined = f"สติรู้เห็น: {thought}"
        return self.deep_reflect(examined, depth - 1)
