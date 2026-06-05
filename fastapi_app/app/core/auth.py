import os
from typing import Annotated

from fastapi import Header, HTTPException


X_QA_SECRET_TOKEN = os.getenv("X_QA_SECRET_TOKEN")

async def verify_qa_token(x_qa_secret_token: str = Header(...)):
    if x_qa_secret_token != X_QA_SECRET_TOKEN:
        raise HTTPException(status_code=401)


async def verify_client_id(client_id: Annotated[int, Header(...)]):
    if client_id is None:
        raise HTTPException(status_code=401)
