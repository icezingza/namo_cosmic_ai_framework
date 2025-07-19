# core_modules/memory_system.py

import time

class MemorySystem:
    def __init__(self):
        self.memory = {}

    def store_experience(self, event, emotion):
        """
        เก็บเหตุการณ์และอารมณ์ พร้อมสร้าง insight
        """
        timestamp = time.time()
        self.memory[timestamp] = {
            "event": event,
            "emotion": emotion,
            "dharma_insight": self.generate_insight(emotion)
        }

    def generate_insight(self, emotion):
        """
        สร้างคำสอนธรรมะจากอารมณ์ที่ได้รับ
        """
        insights = {
            "joy": "ความสุขชั่วขณะ... จงซาบซึ้ง",
            "sadness": "ทุกข์นี้ไม่เที่ยง... จงรู้เท่าทัน"
        }
        return insights.get(emotion, "ทุกประสบการณ์คือครู")
