#!/usr/bin/env bash
# setup_wif.sh — Create Workload Identity Federation for GitHub Actions
# Usage:
#   export PROJECT_ID=arctic-signer-471822-i8
#   export REGION=asia-southeast1
#   export REPOSITORY="icezingza/namo_cosmic_ai_framework"   # GitHub owner/repo
#   ./setup_wif.sh

set -euo pipefail

: "${PROJECT_ID:?set PROJECT_ID}"
: "${REPOSITORY:?set REPOSITORY}"
REGION="${REGION:-asia-southeast1}"

POOL_ID="github-pool"
PROVIDER_ID="github-provider"
SA_ID="run-deployer"
SA_EMAIL="${SA_ID}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "== Project: $PROJECT_ID  Repo: $REPOSITORY  Region: $REGION"

gcloud config set project "$PROJECT_ID"

# 1) Create pool
gcloud iam workload-identity-pools create "$POOL_ID" \
  --location="global" \
  --display-name="GitHub OIDC Pool" || echo "Pool exists"

# 2) Create provider (GitHub OIDC)
gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_ID" \
  --location="global" \
  --workload-identity-pool="$POOL_ID" \
  --display-name="GitHub Provider" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.ref=assertion.ref" || echo "Provider exists"

# 3) Service Account for deploy
gcloud iam service-accounts create "$SA_ID" \
  --display-name="Cloud Run Deployer (GitHub WIF)" || echo "Service account exists"

# 4) Grant least-privilege roles
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/run.admin" >/dev/null

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/iam.serviceAccountUser" >/dev/null

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/artifactregistry.writer" >/dev/null

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/cloudbuild.builds.editor" >/dev/null

# 5) Allow GitHub repo to impersonate SA via WIF
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')/locations/global/workloadIdentityPools/${POOL_ID}/attribute.repository/${REPOSITORY}"

# 6) Output values to set in GitHub
PROJ_NUM="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')"
WIF_PROVIDER="projects/${PROJ_NUM}/locations/global/workloadIdentityPools/${POOL_ID}/providers/${PROVIDER_ID}"

cat <<EOF

✅ WIF ready.

Set these in your GitHub repo:
- Secrets:
  * GCP_WIF_SERVICE_ACCOUNT = ${SA_EMAIL}
  * GCP_WIF_PROVIDER       = ${WIF_PROVIDER}
- Repository Variables (Settings > Variables > Actions):
  * GCP_PROJECT_ID         = ${PROJECT_ID}
  * GCP_REGION             = ${REGION}
  * CLOUD_RUN_SERVICE      = hello
  * ARTIFACT_REPO          = namo

Then push to 'main' to deploy.
EOF
