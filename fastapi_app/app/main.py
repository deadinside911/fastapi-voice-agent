from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve()
path = BASE_DIR.parent.parent / ".env.dev"
loaded = load_dotenv(dotenv_path=path)


from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_session
from core.utils import logging_data_middleware

from routes.calls import router as calls_router
from routes.webhooks import router as webhooks_router

from sockets.status import router as status_router


app = FastAPI()

app.middleware("http")(logging_data_middleware)

app.include_router(calls_router)
app.include_router(webhooks_router)
app.include_router(status_router)


@app.get("/hello-world")
async def hello(session: Annotated[AsyncSession, Depends(get_session)]):
    return {"message": "hello,world!"}
