"""
"""
import hmac
import hashlib
import os

from typing import Annotated

from fastapi import APIRouter, status, Header
from fastapi.responses import JSONResponse

from pydantic import Field


router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)

WEBHOOK_SECRET_KEY = os.getenv("WEBHOOK_SECRET_KEY", "webhook-secret-key").encode("utf-8")


@router.post("/transcripts")
async def transcripts(x_qa_signature: Annotated[str, Header()], message: Annotated[str, Field()]):
    """
    Validates if the message matches the signature in the header
    """
    payload = message.encode("utf-8")

    payload_signature = hmac.new(
        key=WEBHOOK_SECRET_KEY,
        msg=payload,
        digestmod=hashlib.sha256,
    ).hexdigest()

    is_valid = hmac.compare_digest(x_qa_signature, payload_signature)

    if is_valid:
        return JSONResponse({"message": "valid"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse({"message": "invalid"}, status_code=status.HTTP_403_FORBIDDEN)
