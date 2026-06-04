"""
Models implemented in the project
"""
from datetime import datetime
from typing import Annotated

from sqlmodel import SQLModel, Field


class CallerRecord(SQLModel, table=True):
    id: Annotated[int | None, Field(default=None, primary_key=True)]

    agent_id: Annotated[int | None, Field(default=None)]
    agent_politeness_score: Annotated[bool | None, Field(default=None)]

    caller_name: Annotated[str, Field()]
    department: Annotated[str | None, Field()]

    created_at: Annotated[datetime | None, Field(default=datetime.now())]

