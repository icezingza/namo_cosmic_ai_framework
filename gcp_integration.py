import os
from google.cloud import storage, firestore, secretmanager

# Get project ID from environment variables, essential for GCP services
PROJECT_ID = os.getenv("GCP_PROJECT")

# Initialize clients globally to reuse connections
storage_client = storage.Client(project=PROJECT_ID)
firestore_client = firestore.Client(project=PROJECT_ID)
secret_manager_client = secretmanager.SecretManagerServiceClient()

# ---------------- Google Cloud Storage ----------------
def list_gcs_buckets():
    """Lists all GCS buckets in the project."""
    buckets = list(storage_client.list_buckets())
    return [bucket.name for bucket in buckets]

def upload_to_gcs(bucket_name: str, source_file: str, destination_blob: str):
    """Uploads a file to a GCS bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_file)
    return f"Uploaded {source_file} to gs://{bucket_name}/{destination_blob}"

# ---------------- Firestore ----------------
def list_firestore_collections():
    """Lists all top-level collections in Firestore."""
    collections = list(firestore_client.collections())
    return [col.id for col in collections]

def add_firestore_document(collection_name: str, data: dict):
    """Adds a document to a Firestore collection."""
    doc_ref = firestore_client.collection(collection_name).document()
    doc_ref.set(data)
    return f"Document added to {collection_name} with ID: {doc_ref.id}"

# ---------------- Secret Manager ----------------
def access_secret(secret_id: str, version_id: str = "latest"):
    """Accesses a secret from Secret Manager."""
    if not PROJECT_ID:
        raise ValueError("GCP_PROJECT environment variable not set.")
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = secret_manager_client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

# ---------------- Integration Entry ----------------
def gcp_status_check():
    """Checks the status of GCP services by listing GCS buckets."""
    try:
        # Ensure project ID is available
        if not PROJECT_ID:
            return {"error": "GCP_PROJECT environment variable is not set."}
        
        buckets = list_gcs_buckets()
        return {
            "project": PROJECT_ID,
            "status": "ok",
            "buckets": buckets
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # This block is for local testing and won't run in Cloud Run.
    # To test locally, ensure you've set the GCP_PROJECT environment variable
    # and authenticated with `gcloud auth application-default login`.
    if not PROJECT_ID:
        print("Please set the GCP_PROJECT environment variable.")
    else:
        print(f"[NaMo GCP] Running status check for project: {PROJECT_ID}")
        print(gcp_status_check())
