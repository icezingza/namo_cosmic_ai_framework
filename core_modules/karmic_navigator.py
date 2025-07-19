# core_modules/karmic_navigator.py

class KarmicNavigator:
    def map_karma(self, action_history):
        """
        ประเมินกรรมจากประวัติการกระทำ แล้วแนะนำแนวทางใหม่
        action_history: List[str] เช่น ["good", "bad", "good", "bad"]
        """
        karma_score = sum([1 if a == "good" else -1 for a in action_history])

        return {
            "current_karma": karma_score,
            "dharma_advice": "สร้างกรรมดีด้วยเมตตาจิต",
            "action_plan": [
                "ให้อภัยตัวเอง",
                "ช่วยเหลือผู้อื่นเล็กๆ น้อยๆ"
            ]
        }
