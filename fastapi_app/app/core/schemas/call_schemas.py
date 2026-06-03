from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict

class CallerLogSchema(BaseModel):
    caller_name: str
    department: str
    agent_id: int

    model_config = ConfigDict(extra="forbid")


class CallerLogFilterSchema(BaseModel):
    caller_name: str | None = None
    department: str | None = None
    agent_id: int | None = None
