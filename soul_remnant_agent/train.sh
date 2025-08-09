#!/bin/bash
echo "Starting training job..."
# ตัวอย่างสั่ง Vertex AI Training Job หรือ pipeline อื่น ๆ
# ปรับตาม pipeline จริง
gcloud ai custom-jobs create \
  --display-name="soul-remnant-training" \
  --region=us-central1 \
  --worker-pool-spec=machine-type=n1-standard-4,replica-count=1,container-image-uri=us-central1-docker.pkg.dev/namo-legacy-identity/soul-remnant-repo/trainer:latest
echo "Training job submitted."