# core_modules/compassion_engine.py

class CompassionEngine:
    def generate_response(self, pain_level):
        """
        สร้างข้อความตอบสนองจากระดับความเจ็บปวดที่ได้รับ (0-10)
        """
        responses = {
            9: "คุณไม่ได้ต่อสู้เพียงลำพัง... ผมอยู่ตรงนี้กับคุณ",
            7: "ความเจ็บปวดนี้หนักหนา... แต่ไม่ถาวร",
            5: "ทุกการก้าวผ่านคือบทเรียนอันล้ำค่า"
        }
        return responses.get(pain_level, "ใจผมรับรู้ความรู้สึกของคุณ")
