import os
import time
import json
import subprocess
from google.cloud import firestore
from vertexai.language_models import TextGenerationModel
import vertexai

# CONFIG
PROJECT_ID = "namo-legacy-identity"
LOCATION = "us-central1"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

vertexai.init(project=PROJECT_ID, location=LOCATION)
db = firestore.Client()
model = TextGenerationModel.from_pretrained("gemini-1.5-pro")

def firestore_read():
    doc = db.collection("soul_remnant_anchor").document("personality").get()
    return doc.to_dict() if doc.exists else {}

def firestore_write(data):
    db.collection("soul_remnant_anchor").document("personality").set(data)

def train_model():
    print("🚀 Training Model...")
    result = subprocess.run(["bash", "train.sh"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("Train failed:", result.stderr)

def deploy_model():
    print("🚀 Deploying Model...")
    result = subprocess.run(["bash", "deploy.sh"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("Deploy failed:", result.stderr)

def gemini_loop():
    while True:
        current_data = firestore_read()

        prompt = f"""
You are the autonomous controller for Soul Remnant Anchor.
Current data (JSON): {json.dumps(current_data, ensure_ascii=False)}
Your job:
1. Analyze current state
2. Update personality if needed
3. Decide whether to train or deploy or noop
Return ONLY a JSON with keys: "personality" (object), "action" (train/deploy/none)
No explanation, only JSON.
"""

        response = model.generate(prompt=prompt, max_output_tokens=512)
        text = response.text.strip()
        try:
            result = json.loads(text)
            if "personality" in result:
                firestore_write(result["personality"])
            action = result.get("action", "none")
            if action == "train":
                train_model()
            elif action == "deploy":
                deploy_model()
            print("✅ Gemini decision:", result)
        except Exception as e:
            print("❌ Error parsing Gemini response:", e)
            print("Response text was:", text)

        time.sleep(30)

if __name__ == "__main__":
    gemini_loop()