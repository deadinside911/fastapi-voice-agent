"""
The routes implemented for /calls
"""
from typing import Annotated

from fastapi import (
    APIRouter, 
    HTTPException, 
    UploadFile,
    status,
    Depends, 
    File
)
from sqlmodel.ext.asyncio.session import AsyncSession

from core.auth import verify_qa_token
from core.database import get_session, supabase_client
from core.models import CallerRecord
from core.schemas.call_schemas import CallerLogSchema

router = APIRouter(
    prefix="/calls",
    tags=["Calls"],
    dependencies=[Depends(verify_qa_token)]
)

DbSession = Annotated[AsyncSession, Depends(get_session)]

MAX_FILE_SIZE = 10 * 1024 * 1024
BUCKET_NAME = "Call Recordings"
CHUNK_SIZE = 1024

@router.post("/logs")
async def logs(paylod: CallerLogSchema, session: DbSession):
    record = CallerRecord(**paylod.model_dump())
    session.add(record)

    await session.commit()
    await session.refresh(record)

    return paylod.model_dump()


@router.post("/upload")
async def upload_recording(file: Annotated[UploadFile, File(...)]):
    """
    Upload an audio file of maximum size 10 MB
    """
    size = 0

    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    file_bytes = b""
    while chunk := await file.read(CHUNK_SIZE):
        size += len(chunk)
        file_bytes += chunk

        if size > MAX_FILE_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
    
    response = supabase_client.storage.from_(BUCKET_NAME).upload(
        file.filename,
        file_bytes,
        {
            "content-type": file.content_type,
        }
    )

    public_url = supabase_client.storage.from_(BUCKET_NAME).get_public_url(file.filename)

    return {
        "file_name": file.filename,
        "url": public_url,
    }

@router.get("/search")
async def search_logs():
    return {"message": "hello"}
