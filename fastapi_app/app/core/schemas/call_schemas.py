"""
The schemas for the /calls endpoints
"""
from pydantic import BaseModel

class CallerLogSchema(BaseModel):
    """
    The fields needed when creating a new call log
    """
    caller_name: str
    department: str
    agent_id: int

    # Rejects extra fields provided in the request
    model_config = {"extra": "forbid"}


class CallerLogFilterSchema(BaseModel):
    """
    Optional fields that can be used to filter call logs
    """
    caller_name: str | None = None
    department: str | None = None
    agent_id: int | None = None
