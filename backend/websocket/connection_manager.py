from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, code: str, websocket: WebSocket):
        await websocket.accept()

        if code not in self.active_connections:
            self.active_connections[code] = []

        self.active_connections[code].append(websocket)

    def disconnect(self, code: str, websocket: WebSocket):
        self.active_connections[code].remove(websocket)
 
    async def broadcast(self, code: str, message: str):
        for connection in self.active_connections.get(code, []):
            await connection.send_text(message)

    async def close_session(self, code: str):
        connections = self.active_connections.pop(code, [])

        for connection in connections:
            await connection.close()