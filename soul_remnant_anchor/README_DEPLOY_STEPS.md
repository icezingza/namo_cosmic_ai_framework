# ขั้นตอน Deploy

1. ตั้งค่า Google Cloud SDK (`gcloud init`)
2. เปิดบริการ Vertex AI, Firestore, Artifact Registry
3. รัน `python firestore_init.py` เพื่อสร้าง document เริ่มต้น
4. ใช้ `deploy.sh` หรือ `cloudbuild.yaml` เพื่อ build และ deploy