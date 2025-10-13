# NaMo Cosmic AI Framework: Configuration Reference

This document provides a detailed reference for the configuration and environment settings of the NaMo Cosmic AI Framework.

## `config.yaml`

The `config.yaml` file is the primary configuration file for the framework. It contains settings for the model path, runtime environment, logging level, and GCP region.

### Breakdown

```yaml
model_path: models/omega
runtime_env: production
logging_level: info
gcp_region: asia-southeast1
```

*   `model_path`: The path to the directory where the AI models are stored.
*   `runtime_env`: The runtime environment of the application (e.g., `development`, `production`).
*   `logging_level`: The logging level for the application (e.g., `debug`, `info`, `warning`, `error`).
*   `gcp_region`: The Google Cloud region where the application is deployed.

### Preflight Validation

Before deploying the application, it is important to validate the `config.yaml` file to ensure that all the required settings are present and correctly formatted. A pre-flight validation check should be added to the deployment workflow to automate this process.

## `.env` File

The `.env` file is used to store environment variables and secrets. This file should not be committed to version control.

### Example

```
GCP_PROJECT_ID=my-gcp-project
API_KEY=my-secret-api-key
```

## Safety Rules for Environment Setup

*   **Never commit secrets to version control.** Use a `.gitignore` file to exclude the `.env` file from Git.
*   **Use a different `.env` file for each environment.** This will help to prevent accidental use of production secrets in a development environment.
*   **Restrict access to production secrets.** Only authorized personnel should have access to production secrets.

## Troubleshooting

| Error                  | Cause                               | Solution                                                              |
| ---------------------- | ----------------------------------- | --------------------------------------------------------------------- |
| `Config file not found`  | The `config.yaml` file is missing. | Create a `config.yaml` file in the root directory of the project.     |
| `Key not found`          | A required key is missing from the `config.yaml` file. | Add the missing key to the `config.yaml` file.                      |
| `Invalid value`        | A value in the `config.yaml` file is invalid. | Correct the value in the `config.yaml` file.                        |

---
> Author: Jules (AI Automation)
> Verified by: @icezingza
