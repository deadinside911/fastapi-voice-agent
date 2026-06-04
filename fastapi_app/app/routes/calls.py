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
from fastapi.responses import JSONResponse

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.auth import verify_qa_token
from core.database import get_session, supabase_client
from core.models import CallerRecord
from core.schemas.call_schemas import CallerLogSchema, CallerLogFilterSchema

from services.call_services import CallServices, DbSession

router = APIRouter(
    prefix="/calls",
    tags=["Calls"],
    dependencies=[Depends(verify_qa_token)]
)

MAX_FILE_SIZE = 10 * 1024 * 1024
BUCKET_NAME = "Call Recordings"
CHUNK_SIZE = 1024

@router.post("/logs")
async def logs(payload: CallerLogSchema, session: DbSession):
    result = await CallServices.create_log(payload, session)
    return JSONResponse(result, status_code=status.HTTP_200_OK)


@router.post("/upload")
async def upload_recording(file: Annotated[UploadFile, File(...)]):
    """
    Upload an audio file of maximum size 10 MB
    """
    result = await CallServices.upload_recording(file)
    return result


@router.get("/search")
async def search_logs(filter: Annotated[CallerLogFilterSchema, Depends()], session: DbSession):
    """
    Search by optional query parameters
    """
    results = await CallServices.search(filter, session)
    return results
