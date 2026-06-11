"""
Services layer
"""
from typing import Annotated

import os

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from google import genai

from core.database import get_session


DbSession = Annotated[AsyncSession, Depends(get_session)]

client = genai.Client(
    project="curious-set-498810-n8",
    api_key=os.getenv("GEMINI_API_KEY"),
)
