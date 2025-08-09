from google.cloud import firestore

def init_firestore():
    db = firestore.Client()
    db.collection("soul_remnant_anchor").document("personality").set({
        "loop_count": 0,
        "personality_data": {},
        "last_updated": None
    })
    print("Firestore initialized with empty personality.")

if __name__ == "__main__":
    init_firestore()