import time
from google.cloud import firestore

def load_personality(db):
    doc_ref = db.collection("soul_remnant_anchor").document("personality")
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {"status": "empty", "personality_data": {}}

def save_personality(db, data):
    db.collection("soul_remnant_anchor").document("personality").set(data)

def infinite_training_loop():
    db = firestore.Client()
    while True:
        personality = load_personality(db)
        print("Current personality:", personality)
        
        # --- จุดนี้คือที่ต้องใส่ AI logic จริง ---
        # เช่น ดึงข้อมูลจาก dataset, อัปเดต personality, ฯลฯ
        updated = personality.copy()
        updated["loop_count"] = updated.get("loop_count", 0) + 1
        updated["last_updated"] = time.time()

        save_personality(db, updated)
        print("Updated personality:", updated)

        time.sleep(10)  # ปรับความถี่ตามต้องการ

if __name__ == "__main__":
    infinite_training_loop()