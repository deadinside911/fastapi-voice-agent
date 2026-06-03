# Voice QA

Voice QA Fast API project

## Run locally

1. Clone the repo

```zsh
git clone https://github.com/agentblack6000/fastapi-voice-agent.git
```

2. Configure environment variables in the `fastapi_app/` folder

```txt
X_QA_SECRET_TOKEN="..."
DATABASE_URL="..."
DATABASE_URL_SYNC="..."
DATABASE_PASSWORD="..."

SUPABASE_URL="..."
SUPABASE_SERVICE_KEY="..."
```

3. Run the FastAPI project

```zsh
uvicorn main:app --reload
```

or for the Flask app:

```zsh
flask run
```