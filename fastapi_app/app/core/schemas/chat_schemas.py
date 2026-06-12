"""
Message schemas
"""
from pydantic import BaseModel


class ChatModelSchema(BaseModel):
    role: str
    content: str

    model_config = {"extra": "forbid"}
