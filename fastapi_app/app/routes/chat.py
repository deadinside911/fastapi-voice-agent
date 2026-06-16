from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from services.chat_services import ChatServices

from core.schemas.chat_schemas import ChatLogSchema

from . import DbSession

from core.auth import verify_qa_token, verify_client_id

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
    dependencies=[Depends(verify_qa_token), Depends(verify_client_id)],
)


@router.post("/chat")
async def chat_with_model(payload: ChatLogSchema, session: DbSession):

    response = await ChatServices.generate_model_response(
        session=session,
        conversation_id=payload.conversation_id,
        content=payload.content,
    )

    return JSONResponse({ "response": response, }, status_code=200)
