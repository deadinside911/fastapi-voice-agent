"""
Services layer
"""
from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from google import genai

from core.database import get_session


DbSession = Annotated[AsyncSession, Depends(get_session)]

client = genai.Client(
    vertexai=True,
    project="curious-set-498810-n8"
)
