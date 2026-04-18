from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from schemas.session_schema import CreateSessionRequest, JoinSessionRequest
from services.session_service import (
    create_session_service,
    join_session_service
)
from websocket.connection_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

# =========================
# REST endpoints
# =========================

@router.post("/session/create")
def create_session(data: CreateSessionRequest):
    return create_session_service(data.name)


@router.post("/session/join")
def join_session(data: JoinSessionRequest):
    return join_session_service(data.code, data.name)

# =========================
# WebSocket
# =========================

@router.websocket("/ws/{code}")
async def websocket_endpoint(websocket: WebSocket, code: str):
    print("Conectando ao WS...")
    await manager.connect(code, websocket)
    print("WS conectado com sucesso!")

    try:
        while True:
            data = await websocket.receive_text()
            print("Recebido:", data)

            # broadcast para todos da sala
            await manager.broadcast(code, data)

    except WebSocketDisconnect:
        print("WS desconectado")
        manager.disconnect(code, websocket)