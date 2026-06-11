"""
Implement the services needed for the /calls endpoints
"""
from fastapi import (
    HTTPException, 
    UploadFile,
    status,
)

from sqlmodel import select

import tempfile

from core.database import supabase_client, async_supabase_client
from core.models import CallerRecord
from core.schemas.call_schemas import CallerLogSchema, CallerLogFilterSchema

from sockets.manager import websocket_connection_manager

from . import client

from . import DbSession

MAX_FILE_SIZE = 10 * 1024 * 1024
BUCKET_NAME = "Call Recordings"
CHUNK_SIZE = 1024


class CallServices:
    """
    Implement the static methods needed for the /calls endpoints
    """

    @staticmethod
    async def create_log(paylod: CallerLogSchema, session: DbSession, client_id: int):
        """
        Creates a CallerRecord entry and commits it the database
        """

        await websocket_connection_manager.send_message("Creating record", client_id)
        record = CallerRecord(**paylod.model_dump())
        session.add(record)
        
        await websocket_connection_manager.send_message("Updating database", client_id)
        await session.commit()

        return paylod.model_dump()

    @staticmethod
    async def upload_recording(file: UploadFile, client_id: int):
        """
        Uploads an audio recording to the database
        """
        
        # Checks if the file is an audio file
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

        # await websocket_connection_manager.send_message("Valid file type", client_id)

        # Streams the file bytes, stops reading if the file is too large
        size = 0
        file_bytes = b""

        # await websocket_connection_manager.send_message("Uploading file", client_id)
        while chunk := await file.read(CHUNK_SIZE):
            size += len(chunk)
            file_bytes += chunk
            if size > MAX_FILE_SIZE:
                # await websocket_connection_manager.send_message("File too large", client_id)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")
        
        temp_audio_filepath = ""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
            temp_audio_file.write(file_bytes)
            temp_audio_filepath = temp_audio_file.name

        audio_file = client.files.upload(file=temp_audio_filepath)

        # Uploads the file to Supabase
        # try:
        #     # await websocket_connection_manager.send_message("Generating URL...", client_id)
        #     await async_supabase_client.storage.from_(BUCKET_NAME).upload(
        #         file.filename,
        #         file_bytes,
        #         {"content-type": file.content_type}
        #     )
        #     public_url = supabase_client.storage.from_(BUCKET_NAME).get_public_url(file.filename)
        # except Exception:
        #     # await websocket_connection_manager.send_message("Failed", client_id)
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Upload failed to supabase")

        # await websocket_connection_manager.send_message("Done.", client_id)

        gemini_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "Transcrible this audio and prepare a 2 line text summary",
            ]
        )
        # Returns the url of the file from Supabase
        return {"file_name": file.filename, "transcription": gemini_response}

    @staticmethod
    async def search(filter_data: CallerLogFilterSchema, session: DbSession, client_id: int):
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
        
        await websocket_connection_manager.send_message("Fetching results", client_id)
        results = await session.exec(query)
        
        await websocket_connection_manager.send_message("Done.", client_id)
        return results.all() 

