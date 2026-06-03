import os

from fastapi import Header, HTTPException

X_QA_SECRET_TOKEN = os.getenv("X_QA_SECRET_TOKEN")

async def verify_qa_token(x_qa_secret_token: str = Header(...)):
    if x_qa_secret_token != X_QA_SECRET_TOKEN:
        raise HTTPException(status_code=401)