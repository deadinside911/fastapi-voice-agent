from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .manager import websocket_connection_manager

router = APIRouter(
    prefix="/ws",
    tags=["WebSockets"],
)


@router.websocket("/status")
async def status(websocket: WebSocket):
    await websocket_connection_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket_connection_manager.send_broadcast(f"Recieved {data}")
    except WebSocketDisconnect:
        websocket_connection_manager.disconnect(websocket)
        print("Disconnected gracefully")

