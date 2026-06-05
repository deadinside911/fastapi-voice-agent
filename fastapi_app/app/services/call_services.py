"""
Implement the services needed for the /calls endpoints
"""
from fastapi import (
    HTTPException, 
    UploadFile,
    status,
)

from sqlmodel import select

from core.database import supabase_client
from core.models import CallerRecord
from core.schemas.call_schemas import CallerLogSchema, CallerLogFilterSchema

from . import DbSession

MAX_FILE_SIZE = 10 * 1024 * 1024
BUCKET_NAME = "Call Recordings"
CHUNK_SIZE = 1024


class CallServices:
    """
    Implement the static methods needed for the /calls endpoints
    """

    @staticmethod
    async def create_log(paylod: CallerLogSchema, session: DbSession):
        """
        Creates a CallerRecord entry and commits it the database
        """
        record = CallerRecord(**paylod.model_dump())
        session.add(record)

        await session.commit()

        return paylod.model_dump()

    @staticmethod
    async def upload_recording(file: UploadFile):
        """
        Uploads an audio recording to the database
        """
        
        # Checks if the file is an audio file
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

        # Streams the file bytes, stops reading if the file is too large
        size = 0
        file_bytes = b""
        while chunk := await file.read(CHUNK_SIZE):
            size += len(chunk)
            file_bytes += chunk
            if size > MAX_FILE_SIZE:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")
            
        # Uploads the file to Supabase
        try:
            supabase_client.storage.from_(BUCKET_NAME).upload(
                file.filename,
                file_bytes,
                {"content-type": file.content_type}
            )
            public_url = supabase_client.storage.from_(BUCKET_NAME).get_public_url(file.filename)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Upload failed")

        # Returns the url of the file from Supabase
        return {"file_name": file.filename, "public_url": public_url}

    @staticmethod
    async def search(filter_data: CallerLogFilterSchema, session: DbSession):
        """
        """
        filters = {
            key: value 
            for key, value in filter_data.model_dump().items() 
            if value is not None
        }
        
        query = (
            select(CallerRecord)
            .filter_by(**filters)
            .order_by(CallerRecord.created_at.desc())
        )
        
        results = await session.exec(query)
        return results.all() 

