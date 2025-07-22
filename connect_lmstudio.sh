#!/bin/bash

echo "🚀 กำลังเช็ค LM Studio API endpoint..."
LM_ENDPOINT="http://127.0.0.1:1234/v1"

# เช็คว่า LM Studio เปิดอยู่ไหม
if curl -s --head $LM_ENDPOINT | grep "200 OK" > /dev/null; then
    echo "✅ พบ LM Studio รันที่ $LM_ENDPOINT"
else
    echo "❌ ไม่พบ LM Studio API ที่ $LM_ENDPOINT"
    echo "กรุณาเปิด LM Studio แล้วโหลดโมเดลก่อน เช่น liquid/lfm2-1.2b"
    exit 1
fi

echo "📝 แก้ไขไฟล์ .env เพื่อเชื่อมต่อกับ LM Studio..."
# สำรองไฟล์เดิมก่อน
cp .env .env.backup

# เปลี่ยน API base URL
sed -i 's|^OPENAI_API_BASE=.*|OPENAI_API_BASE='"$LM_ENDPOINT"'|' .env

echo "🔄 รีสตาร์ท NaMo Cosmic AI Framework..."
docker compose down
docker compose up -d

echo "🎉 เสร็จสิ้น! NaMo ตอนนี้เชื่อมกับ LM Studio แล้ว"
echo "🌐 เปิด WebUI ที่: http://localhost:7860 หรือ Cloud Run URL เดิม"
echo "💡 ถ้าอยากกลับไปใช้ OpenAI API ให้เรียกคืน .env.backup"
