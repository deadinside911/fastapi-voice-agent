"""
Webhook endpoints
"""
from typing import Annotated

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import Field

from services.webhook_services import WebhookServices


router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)


@router.post("/transcripts")
async def transcripts(request: Request, message: Annotated[str, Field()]):
    """
    Validates if the message matches the signature in the header
    """
    try:
        request_signature = request.headers[WebhookServices.signature_header]
    except KeyError:
        return JSONResponse({"message": "Invalid request structure"}, status_code=status.HTTP_400_BAD_REQUEST)

    is_valid = WebhookServices.validate_signature(message=message, signature=request_signature)

    if is_valid:
        return JSONResponse({"message": "valid"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse({"message": "invalid"}, status_code=status.HTTP_403_FORBIDDEN)
