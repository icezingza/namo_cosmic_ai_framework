# CI/CD via GitHub Actions + Workload Identity Federation (no JSON keys)

## Quickstart
1) On GCP, run:
```bash
PROJECT_ID=arctic-signer-471822-i8 \
REPOSITORY=icezingza/namo_cosmic_ai_framework \
REGION=asia-southeast1 \
bash scripts/setup_wif.sh
```

2) In GitHub repo **Settings**:
- Secrets ➜
  - `GCP_WIF_SERVICE_ACCOUNT` = `run-deployer@arctic-signer-471822-i8.iam.gserviceaccount.com`
  - `GCP_WIF_PROVIDER` = `projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/github-pool/providers/github-provider`
- Variables ➜
  - `GCP_PROJECT_ID` = `arctic-signer-471822-i8`
  - `GCP_REGION` = `asia-southeast1`
  - `CLOUD_RUN_SERVICE` = `hello`
  - `ARTIFACT_REPO` = `namo`

3) Push โค้ดขึ้น branch `main` → Action จะ build image (Cloud Build) และ deploy ไป Cloud Run อัตโนมัติ

> หมายเหตุ: ครั้งแรกอาจต้อง enable APIs; workflow ทำให้แล้วแบบ idempotent
