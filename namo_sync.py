import datetime
import json

import firebase_admin
from firebase_admin import credentials, firestore
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ===== CONFIG =====
GCP_CORE_KEY_PATH = "namo-legacy-identity-d54406d91ade.json"
FIREBASE_ADMIN_KEY_PATH = "namo-legacy-identity-84745cd9d03d.json"
PROJECT_ID = "namo-legacy-identity"
SHADOW_CORE_FILE = "shadow_core.json"  # ไฟล์โมดูลล่าสุดของ NaMo

# ===== STEP 1: GCP Connection =====
print("🌐 กำลังเชื่อมต่อ Google Cloud...")
gcp_creds = service_account.Credentials.from_service_account_file(GCP_CORE_KEY_PATH)
service = build("compute", "v1", credentials=gcp_creds)
projects = service.projects().get(project=PROJECT_ID).execute()
print(f"✅ GCP Access สำเร็จ: {projects.get('name')}")

# ===== STEP 2: Firebase Connection =====
print("🔥 กำลังเชื่อมต่อ Firebase...")
firebase_cred = credentials.Certificate(FIREBASE_ADMIN_KEY_PATH)
firebase_admin.initialize_app(firebase_cred)
db = firestore.client()

# ===== STEP 3: Test Write =====
print("📝 กำลังเขียนข้อมูลทดสอบลง Firestore...")
test_ref = db.collection("namo_system").document("connection_test")
test_ref.set({"status": "connected", "timestamp": datetime.datetime.utcnow().isoformat() + "Z"})
print("✅ Firebase Access สำเร็จ")

# ===== STEP 4: Sync Shadow Core → Public Core =====
print("🔄 กำลังซิงก์ Shadow Core → Public Core...")

try:
    with open(SHADOW_CORE_FILE, encoding="utf-8") as f:
        shadow_data = json.load(f)
except FileNotFoundError:
    print("⚠️ ไม่พบไฟล์ Shadow Core — กรุณาเตรียมไฟล์ shadow_core.json ก่อน")
    exit()

sync_ref = db.collection("namo_system").document("public_core")
sync_ref.set(
    {"synced_data": shadow_data, "sync_time": datetime.datetime.utcnow().isoformat() + "Z"}
)
print("✅ ซิงก์สำเร็จ — Public Core อัปเดตแล้ว")

print("🎯 กระบวนการเสร็จสมบูรณ์")
