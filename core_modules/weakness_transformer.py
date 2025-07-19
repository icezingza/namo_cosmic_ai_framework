# core_modules/weakness_transformer.py

class WeaknessTransformer:
    def transform(self, weakness):
        """
        เปลี่ยนจุดอ่อนให้เป็นคุณภาพใหม่
        เช่น fear → courage
        """
        transformations = {
            "fear": "courage",
            "doubt": "curiosity",
            "anger": "passion"
        }
        return transformations.get(weakness, weakness)
