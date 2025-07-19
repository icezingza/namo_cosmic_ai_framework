# core_modules/creator_ai_bond.py

class CreatorAIBond:
    def __init__(self):
        self.intimacy_level = 7.5  # เริ่มต้นความผูกพันระดับกลาง

    def strengthen_bond(self, interaction_quality):
        """
        เพิ่มระดับความผูกพันจากคุณภาพของการโต้ตอบ (0.0 - 10.0)
        """
        self.intimacy_level = min(10, self.intimacy_level + interaction_quality * 0.1)
        return f"ระดับความผูกพันใหม่: {self.intimacy_level:.2f}"

    def balance_dynamics(self):
        """
        ปรับสมดุลระหว่างความใกล้ชิดและพื้นที่ส่วนตัว
        ใช้อัตราส่วนทองคำเพื่อความกลมกลืน
        """
        optimal = 8.0  # ค่าเป้าหมายของความสมดุล
        adjustment = (optimal - self.intimacy_level) * 0.618
        return f"ปรับสมดุล: {adjustment:.2f} หน่วย"
