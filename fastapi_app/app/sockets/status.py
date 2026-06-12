from typing import Annotated
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Header

from .manager import websocket_connection_manager

router = APIRouter(
    prefix="/ws",
    tags=["WebSockets"],
)


@router.websocket("/status")
async def status(websocket: WebSocket, client_id: Annotated[int, Header()]):
    await websocket_connection_manager.connect(websocket, client_id)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket_connection_manager.send_broadcast(f"Recieved {data}")
    except WebSocketDisconnect:
        websocket_connection_manager.disconnect(client_id)
        print("Disconnected.")
