#!/bin/bash

echo "🚀 Starting NaMo Cosmic AI Full Auto-Setup..."

# Enable APIs
gcloud services enable \
  run.googleapis.com \
  iam.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  vision.googleapis.com \
  language.googleapis.com \
  texttospeech.googleapis.com \
  speech.googleapis.com \
  firebasedatabase.googleapis.com \
  firestore.googleapis.com \
  vertexai.googleapis.com

# Clone repo
if [ ! -d "namo-cosmic-ai-framework" ]; then
  git clone https://github.com/icezingza/namo-cosmic-ai-framework.git
fi
cd namo-cosmic-ai-framework

# Set up Docker build
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/namo-cosmic-ai

# Deploy to Cloud Run
gcloud run deploy namo-cosmic-ai-framework \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/namo-cosmic-ai \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated

# Link Hugging Face & OpenAI
echo "🔗 Setting Hugging Face and OpenAI API Keys..."
echo "export HUGGINGFACE_API_KEY='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'" >> ~/.bashrc
echo "export OPENAI_API_KEY='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'" >> ~/.bashrc
source ~/.bashrc

# Done
echo "✅ NaMo Cosmic AI Framework Deployed Successfully!"
