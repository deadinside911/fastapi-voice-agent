"""
"""
from typing import Annotated

from fastapi import (
    HTTPException, 
    UploadFile,
    status,
    Depends,
)

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_session, supabase_client
from core.models import CallerRecord
from core.schemas.call_schemas import CallerLogSchema, CallerLogFilterSchema


MAX_FILE_SIZE = 10 * 1024 * 1024
BUCKET_NAME = "Call Recordings"
CHUNK_SIZE = 1024

DbSession = Annotated[AsyncSession, Depends(get_session)]

class CallServices:
    """
    """

    @staticmethod
    async def create_log(paylod: CallerLogSchema, session: DbSession):
        """
        """
        record = CallerRecord(**paylod.model_dump())
        session.add(record)

        await session.commit()
        await session.refresh(record)

        return paylod.model_dump()

    @staticmethod
    async def upload_recording(file: UploadFile):
        """
        """
        size = 0
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

        file_bytes = b""
        while chunk := await file.read(CHUNK_SIZE):
            size += len(chunk)
            file_bytes += chunk
            if size > MAX_FILE_SIZE:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")
            
        try:
            supabase_client.storage.from_(BUCKET_NAME).upload(
                file.filename,
                file_bytes,
                {"content-type": file.content_type}
            )
            public_url = supabase_client.storage.from_(BUCKET_NAME).get_public_url(file.filename)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Upload failed")

        return {"file_name": file.filename, "public_url": public_url}

    @staticmethod
    async def search(filter_data: CallerLogFilterSchema, session: DbSession):
        """
        """
        query = select(CallerRecord)

        if filter_data.department is not None:
            query = query.where(CallerRecord.department == filter_data.department)
        if filter_data.caller_name is not None:
            query = query.where(CallerRecord.caller_name == filter_data.caller_name)
        if filter_data.agent_id is not None:
            query = query.where(CallerRecord.agent_id == filter_data.agent_id)

        query = query.order_by(CallerRecord.created_at.desc())
        results = await session.execute(query)
        return results.scalars().all()

