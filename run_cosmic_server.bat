@echo off
echo 🚀 Starting NaMo Cosmic AI Framework Server...
call python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
