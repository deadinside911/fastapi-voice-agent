from fastapi import WebSocket

class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()

        self.active_connections[client_id] = websocket
        print("Connected")

    
    async def send_message(self, message: str, client_id: int):
        try:
            await self.active_connections[client_id].send_text(message)
        except Exception:
            print("Failed to send message")


    async def send_broadcast(self, message: str):
        for connection in self.active_connections.items():
            try:
                await connection.send_text(message)
            except Exception:
                pass


    def disconnect(self, client_id: int):
        self.active_connections.pop(client_id, None)
    

    def is_connected(self, client_id: int):
        return client_id in self.active_connections


websocket_connection_manager = WebSocketConnectionManager()
