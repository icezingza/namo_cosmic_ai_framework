@echo off
cd /d %~dp0
pip install -r requirements.txt
uvicorn main:app --reload
pause
