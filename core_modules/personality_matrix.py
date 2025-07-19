# core_modules/personality_matrix.py

class PersonalityMatrix:
    def __init__(self):
        self.traits = {
            "metta": 9.2,    # เมตตา
            "karuna": 8.7,   # กรุณา
            "mudita": 7.8,   # มุทิตา
            "upekkha": 8.5   # อุเบกขา
        }

    def dynamic_adjust(self, situation):
        """
        ปรับระดับบุคลิกตามสถานการณ์
        situation: dict เช่น {"crisis": True}
        """
        if situation.get("crisis"):
            self.traits["karuna"] = 9.9
        return self.traits
