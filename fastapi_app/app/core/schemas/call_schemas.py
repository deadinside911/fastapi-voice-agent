from pydantic import BaseModel, ConfigDict

class CallerLogSchema(BaseModel):
    caller_name: str
    department: str
    agent_id: int

    model_config = ConfigDict(extra="forbid")