# NaMo Cosmic AI Framework: Deployment Notes

This guide provides instructions for deploying and maintaining the NaMo Cosmic AI Framework.

## Google Cloud Run Deployment

The following steps outline how to deploy the framework to Google Cloud Run:

1.  **Authenticate with Google Cloud:**

    ```bash
    gcloud auth login
    gcloud config set project [YOUR_PROJECT_ID]
    ```

2.  **Deploy the service:**

    ```bash
    gcloud run deploy namo-omega \
      --source . \
      --platform managed \
      --region asia-southeast1 \
      --allow-unauthenticated
    ```

## CI/CD Automation

The `.github/workflows/deploy.yml` file contains the GitHub Actions workflow for automating the deployment of the framework to Google Cloud Run. This workflow is triggered on pushes to the `main` branch.

## Local Testing

Before deploying the framework, it is recommended to run the following local tests:

1.  **Run the test suite:**

    ```bash
    pytest
    ```

2.  **Check the `/health` endpoint:**

    Start the application locally and then run the following command:

    ```bash
    curl http://localhost:8000/health
    ```

## Scaling Configuration

The following scaling configuration options are available for the Google Cloud Run service:

*   **Memory**: The amount of memory allocated to each container instance.
*   **Concurrency**: The maximum number of concurrent requests that can be sent to a container instance.
*   **Autoscaling**: The minimum and maximum number of container instances to run.

These settings can be configured in the `cloudbuild.yaml` file or through the Google Cloud Console.

## Maintenance and Rollback

### Maintenance

To update the service, simply push the new code to the `main` branch. The CI/CD workflow will automatically deploy the new version.

### Rollback

To roll back to a previous version of the service, you can use the `gcloud run services update` command with the `--to-revisions` flag.

---
> Author: Jules (AI Automation)
> Verified by: @icezingza
