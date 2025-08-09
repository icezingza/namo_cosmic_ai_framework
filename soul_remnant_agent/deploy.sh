#!/bin/bash
echo "Starting deploy job..."
# ตัวอย่าง deploy โมเดลหรือ container อัตโนมัติ
gcloud run deploy soul-remnant-service \
  --image us-central1-docker.pkg.dev/namo-legacy-identity/soul-remnant-repo/soul-remnant:latest \
  --region us-central1 \
  --platform managed \
  --quiet
echo "Deploy completed."