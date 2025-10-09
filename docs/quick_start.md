# Infinity AI Framework Quick Start

1. Clone the repository and install dependencies:

```bash
git clone https://github.com/your-org/infinity-ai-framework.git
cd infinity-ai-framework
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the unit tests:

```bash
pytest -q
```

3. Launch the REST API locally:

```bash
uvicorn api.rest_api:app --reload
```

4. Explore the API documentation at `http://localhost:8000/docs`.
