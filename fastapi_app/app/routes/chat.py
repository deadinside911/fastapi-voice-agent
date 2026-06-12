from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


from core.auth import verify_qa_token, verify_client_id

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
    dependencies=[Depends(verify_qa_token), Depends(verify_client_id)],
)


@router.post("/chat")
def chat_with_model():
    return JSONResponse("hello", status_code=200)
