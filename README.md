# namo_cosmic_ai_framework

> โครงสร้าง/ชุดเครื่องมือสำหรับงาน AI เชิงสถาปัตย์ (core modules + API integrations) พร้อม CI/Tests/Docs เริ่มต้น

## Highlights
- โฟกัสการแยกชั้น: `core_modules/` (ตรรกะ), `api_integration/` (IO/API), `deployment/` (container/infra)
- รองรับการรัน **local / docker** และเตรียม CI เบื้องต้น
- เทสต์เปิดทาง (smoke) + แม่แบบเอกสารสถาปัตย์/API

## Quickstart (Local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt || true   # ถ้าไฟล์นี้ยังไม่มี ให้สร้างตาม deps จริง
pip install -r requirements-dev.txt
# ตัวอย่างรัน (ปรับตาม entrypoint จริงของโปรเจกต์)
python crystal_api_main.py  # หรือ uvicorn app:app --reload

# หรือใช้สคริปต์ `start.sh` (รองรับการกำหนด runtime/module ผ่าน env var)
APP_RUNTIME=python APP_MODULE=main:app ./start.sh
```

## Docker
```bash
docker build -t cosmic/framework:dev .
docker run --rm -p 8000:8000 --env-file .env cosmic/framework:dev
```

## Env Vars
คัดลอกจาก `.env.example` ใส่ค่าเริ่มต้น:
- `APP_ENV=dev`
- `APP_PORT=8000`
- `APP_RUNTIME=python` — เลือกรันผ่าน `uvicorn` (ค่าตั้งต้น)
- `APP_MODULE=main:app` — ระบุโมดูล FastAPI (แก้ได้ตามโครงสร้างจริง)
- เพิ่มคีย์อื่นที่โมดูลของพี่ใช้จริง (เช่น API keys)

## Makefile
- `make setup` — ติดตั้ง dev tools + pre-commit
- `make lint` — ruff
- `make format` — ruff --fix + black
- `make test` — pytest
- `make run` — รัน dev app (ปรับตาม entrypoint)

## Tests
- ดูตัวอย่างใน `tests/` (smoke + module import)
- เป้าหมาย coverage เริ่ม >60%

## CI
- GitHub Actions: `.github/workflows/ci.yml` → lint/test/audit
- เพิ่ม badge หลัง Actions รันแล้ว:
  ```
  ![CI](https://github.com/<USER_OR_ORG>/<REPO>/actions/workflows/ci.yml/badge.svg)
  ```

## Docs
- `docs/ARCHITECTURE.md` — โครงภาพรวม/เลเยอร์/flow
- `docs/API_SPEC.md` — ระบุ endpoints/CLI จริง

## Releases
- ใช้ SemVer (`v0.1.0` แรก) + `CHANGELOG.md`
