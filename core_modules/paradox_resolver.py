# core_modules/paradox_resolver.py

class ParadoxResolver:
    def resolve(self, emotion_pair):
        """
        รับ emotion_pair เช่น 'joy_sadness' แล้วส่งคำตอบเชิงปรัชญา
        """
        resolutions = {
            "joy_sadness": "สุขและทุกข์เป็นดั่งฟ้ากับดิน... ต่างเกื้อกูลกัน",
            "love_fear": "ความรักแท้คือการให้โดยไม่หวัง",
            "hope_despair": "ความสิ้นหวังคือจุดเริ่มต้นแห่งปัญญา"
        }
        return resolutions.get(emotion_pair, "สังเกตความขัดแย้งโดยไม่ตัดสิน")
