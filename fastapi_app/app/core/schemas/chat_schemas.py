"""
Message schemas
"""
from pydantic import BaseModel

class ChatLogSchema(BaseModel):
    conversation_id: str        
    role: str
    content: str
    model_config = {"extra": "forbid"}

class ChatResponseSchema(BaseModel):
    response: str