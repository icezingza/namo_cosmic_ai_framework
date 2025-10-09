# Namo Cosmic AI Memory Service

> API Service สำหรับจัดการ Memory ของ AI Agent ที่สร้างบน FastAPI และทำงานร่วมกับ Google Firestore ได้อย่างสมบูรณ์

## ภาพรวม

โปรเจกต์นี้คือ Backend Service ที่พร้อมใช้งาน (Production-Ready) สำหรับเป็น "Tool" ให้กับ AI Agent (เช่น Custom GPT) ในการจดจำและเรียกใช้ประวัติการสนทนา โดยมีคุณสมบัติดังนี้:

-   **FastAPI:** สร้าง API ที่รวดเร็วและมีเอกสารอัตโนมัติ (Swagger UI / ReDoc)
-   **Google Firestore Integration:** ใช้ Firestore เป็นฐานข้อมูลสำหรับจัดเก็บบทสนทนา
-   **Application Default Credentials (ADC):** ออกแบบมาเพื่อทำงานบน Google Cloud (เช่น Cloud Run) ได้อย่างง่ายดายและปลอดภัย โดยไม่ต้องจัดการกับไฟล์ Service Account Key โดยตรง
-   **Production-Ready:** มี Health Check endpoint และโครงสร้างที่ง่ายต่อการนำไปใช้งาน

## Quickstart (Local Development)

### 1. ตั้งค่า Environment
```bash
# สร้างและเปิดใช้งาน Virtual Environment
python -m venv .venv
source .venv/bin/activate

# ติดตั้ง Dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
# ตัวอย่างรัน (ปรับตาม entrypoint จริงของโปรเจกต์)
python crystal_api_main.py  # หรือ uvicorn app:app --reload

# หรือใช้สคริปต์ `start.sh` (รองรับการกำหนด runtime/module ผ่าน env var)
APP_RUNTIME=python APP_MODULE=main:app ./start.sh
```

### 2. ตั้งค่า Google Cloud Authentication
ในการรันบนเครื่อง Local คุณต้องยืนยันตัวตนกับ Google Cloud ก่อน
```bash
# ล็อกอินด้วย gcloud CLI
gcloud auth application-default login

# ตั้งค่าโปรเจกต์ (แทนที่ YOUR_PROJECT_ID ด้วย GCP Project ID ของคุณ)
gcloud config set project YOUR_PROJECT_ID
```

### 3. ตั้งค่า Environment Variables
สร้างไฟล์ `.env` และเพิ่มตัวแปรที่จำเป็น:
```
# .env
GCP_PROJECT_ID="YOUR_PROJECT_ID"
```

### 4. รัน API Server
```bash
# รันเซิร์ฟเวอร์ด้วย Uvicorn
uvicorn crystal_api_main:app --reload --port 8000
```

## Env Vars
คัดลอกจาก `.env.example` ใส่ค่าเริ่มต้น:
- `APP_ENV=dev`
- `APP_PORT=8000`
- `APP_RUNTIME=python` — เลือกรันผ่าน `uvicorn` (ค่าตั้งต้น)
- `APP_MODULE=main:app` — ระบุโมดูล FastAPI (แก้ได้ตามโครงสร้างจริง)
- เพิ่มคีย์อื่นที่โมดูลของพี่ใช้จริง (เช่น API keys)

## Makefile
-   `make setup` — ติดตั้ง dev tools + pre-commit
-   `make lint` — รัน linter (ruff)
-   `make format` — จัดรูปแบบโค้ด (ruff --fix + black)
-   `make test` — รัน unit tests (pytest)
-   `make run` — รัน dev app (uvicorn)