# NaMo Cosmic AI Framework: API Usage Guide

This guide provides a comprehensive reference for interacting with the NaMo Cosmic AI Framework API.

## Base URL

All API endpoints are relative to the following base URL:

`https://namo-omega-185116032835.asia-southeast1.run.app`

## Endpoints

### `POST /cosmic-intelligence`

This endpoint is used for reasoning and blueprint generation.

*   **Method**: `POST`
*   **URL**: `/cosmic-intelligence`
*   **Description**: Submits a query to the Cosmic Intelligence Core to generate a cosmic blueprint.

#### Input Schema (JSON)

```json
{
  "query": "string"
}
```

#### Output Schema (JSON)

```json
{
  "blueprint": "string"
}
```

#### Example `curl` Command

```bash
curl -X POST "https://namo-omega-185116032835.asia-southeast1.run.app/cosmic-intelligence" \
-H "Content-Type: application/json" \
-d '{"query":"Generate cosmic blueprint"}'
```

### `GET /health`

This endpoint is used to check the service status.

*   **Method**: `GET`
*   **URL**: `/health`
*   **Description**: Returns the health status of the service.

#### Output Schema (JSON)

```json
{
  "status": "ok"
}
```

#### Example `curl` Command

```bash
curl "https://namo-omega-185116032835.asia-southeast1.run.app/health"
```

## Example Python Call

Here's an example of how to call the `/cosmic-intelligence` endpoint using the `requests` library in Python:

```python
import requests
import json

base_url = "https://namo-omega-185116032835.asia-southeast1.run.app"
endpoint = "/cosmic-intelligence"

headers = {
    "Content-Type": "application/json"
}

data = {
    "query": "Generate cosmic blueprint"
}

response = requests.post(f"{base_url}{endpoint}", headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("Success:")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

## Authentication

Currently, the API does not require authentication. However, API key authentication may be implemented in the future. Please refer to this documentation for updates.

---
> Author: Jules (AI Automation)
> Verified by: @icezingza
