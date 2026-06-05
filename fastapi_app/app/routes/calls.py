"""
The endpoints implemented for /calls
"""
from typing import Annotated

from fastapi import (
    APIRouter, 
    UploadFile,
    status,
    Depends, 
    File,
    Header,
)
from fastapi.responses import JSONResponse

from core.auth import verify_qa_token, verify_client_id
from core.schemas.call_schemas import CallerLogSchema, CallerLogFilterSchema

from services.call_services import CallServices, DbSession

# Configures the /calls router, ensures that all incoming requests
# have a valid header
router = APIRouter(
    prefix="/calls",
    tags=["Calls"],
    dependencies=[Depends(verify_qa_token), Depends(verify_client_id)]
)


@router.post("/logs")
async def logs(payload: CallerLogSchema, session: DbSession, client_id: Annotated[int, Header(...)]):
    """
    Creates a log based on the request data and uploads it to the database
    """
    result = await CallServices.create_log(payload, session, client_id)
    return JSONResponse(result, status_code=status.HTTP_200_OK)


@router.post("/upload")
async def upload_recording(file: Annotated[UploadFile, File(...)], client_id: Annotated[int, Header(...)]):
    """
    Upload an audio file of maximum size 10 MB to a Supabase bucket
    """
    result = await CallServices.upload_recording(file, client_id)
    return result


@router.get("/search")
async def search_logs(filter: Annotated[CallerLogFilterSchema, Depends()], session: DbSession, client_id: Annotated[int, Header(...)]):
    """
    Search by optional query parameters
    """
    results = await CallServices.search(filter, session, client_id)
    return results
