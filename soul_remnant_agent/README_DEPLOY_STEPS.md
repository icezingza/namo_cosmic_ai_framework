# Soul Remnant Anchor - Gemini Agent Deployment Guide

## 1. เตรียม GCP Project
- ตั้งค่า Project ID: namo-legacy-identity
- เปิด API:
  - AI Platform (Vertex AI)
  - Firestore
  - Cloud Run
  - Artifact Registry
  - Cloud Build

## 2. สร้าง Service Account
```bash
gcloud iam service-accounts create gemini-agent --display-name "Gemini Autonomous Agent"
gcloud projects add-iam-policy-binding namo-legacy-identity \
  --member="serviceAccount:gemini-agent@namo-legacy-identity.iam.gserviceaccount.com" \
  --role="roles/aiplatform.admin"
gcloud projects add-iam-policy-binding namo-legacy-identity \
  --member="serviceAccount:gemini-agent@namo-legacy-identity.iam.gserviceaccount.com" \
  --role="roles/datastore.user"
gcloud iam service-accounts keys create key.json \
  --iam-account gemini-agent@namo-legacy-identity.iam.gserviceaccount.com