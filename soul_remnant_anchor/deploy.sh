#!/bin/bash
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
REPO_NAME="soul-remnant-anchor"
IMAGE_NAME="soul_remnant_anchor_image"

# Enable services
gcloud services enable artifactregistry.googleapis.com aiplatform.googleapis.com firestore.googleapis.com

# Create Artifact Registry repo
gcloud artifacts repositories create $REPO_NAME \
  --repository-format=docker \
  --location=$REGION \
  --description="Soul Remnant Anchor Images" || true

# Build and push image
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME .

# Run custom job on Vertex AI
gcloud ai custom-jobs create \
  --region=$REGION \
  --display-name="soul-remnant-anchor-job" \
  --worker-pool-spec=machine-type=n1-standard-4,replica-count=1,container-image-uri=$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME