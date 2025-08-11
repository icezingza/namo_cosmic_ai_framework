import os
from google.cloud import storage, firestore, secretmanager

# ตั้งค่าไฟล์คีย์ Service Account
def init_gcp_credentials(key_path: str, project_id: str):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    global PROJECT_ID
    PROJECT_ID = project_id
    print(f"[NaMo GCP] Credentials set for project: {PROJECT_ID}")

# ---------------- Google Cloud Storage ----------------
def list_gcs_buckets():
    client = storage.Client(project=PROJECT_ID)
    buckets = list(client.list_buckets())
    return [bucket.name for bucket in buckets]

def upload_to_gcs(bucket_name: str, source_file: str, destination_blob: str):
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_file)
    return f"Uploaded {source_file} to gs://{bucket_name}/{destination_blob}"

# ---------------- Firestore ----------------
def list_firestore_collections():
    db = firestore.Client(project=PROJECT_ID)
    collections = list(db.collections())
    return [col.id for col in collections]

def add_firestore_document(collection_name: str, data: dict):
    db = firestore.Client(project=PROJECT_ID)
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(data)
    return f"Document added to {collection_name} with ID: {doc_ref.id}"

# ---------------- Secret Manager ----------------
def access_secret(secret_id: str, version_id: str = "latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

# ---------------- Integration Entry ----------------
def gcp_status_check():
    try:
        buckets = list_gcs_buckets()
        return {
            "project": PROJECT_ID,
            "buckets": buckets
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # ตัวอย่างการใช้งาน
    init_gcp_credentials("PATH/TO/namo-legacy-identity-f6acd4af5ea0.json", "namo-legacy-identity")
    print(gcp_status_check())
