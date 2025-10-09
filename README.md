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

เมื่อเซิร์ฟเวอร์ทำงานแล้ว คุณสามารถเข้าถึง API ได้ที่ `http://127.0.0.1:8000`

## API Documentation
เอกสาร API จะถูกสร้างขึ้นโดยอัตโนมัติโดย FastAPI:
-   **Swagger UI:** `http://127.0.0.1:8000/docs`
-   **ReDoc:** `http://127.0.0.1:8000/redoc`

## Docker
ในการรันด้วย Docker คุณต้องส่ง Environment Variable เข้าไปใน Container
```bash
# 1. Build the image
docker build -t cosmic/memory-service:latest .

# 2. Run the container
docker run --rm -p 8000:8000 \
  -e GCP_PROJECT_ID="YOUR_PROJECT_ID" \
  --name memory_service \
  cosmic/memory-service:latest
```
**หมายเหตุ:** สำหรับการใช้งานบน Docker ที่ไม่ได้รันบน GCP environment, คุณอาจต้อง Mount Service Account Key file และตั้งค่า `GOOGLE_APPLICATION_CREDENTIALS` environment variable เพิ่มเติม

## Makefile
-   `make setup` — ติดตั้ง dev tools + pre-commit
-   `make lint` — รัน linter (ruff)
-   `make format` — จัดรูปแบบโค้ด (ruff --fix + black)
-   `make test` — รัน unit tests (pytest)
-   `make run` — รัน dev app (uvicorn)