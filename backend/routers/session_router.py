from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from core.session_store import sessions
from schemas.session_schema import CreateSessionRequest, JoinSessionRequest
from services.session_service import (
    create_session_service,
    join_session_service,
    save_vote,
    reveal_votes,
    reset_votes,
    delete_session_service,
    get_session_state,
    leave_session_service
)
from websocket.connection_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

# =========================
# REST endpoints
# =========================

@router.post("/session/create")
def create_session(data: CreateSessionRequest):
    return create_session_service(
        data.session_name,
        data.admin_name
    )

@router.post("/session/join")
def join_session(data: JoinSessionRequest):
    return join_session_service(data.code, data.name)

@router.get("/session/{code}")
def get_session(code: str):

    if code not in sessions:
        return {"error": "Sessão não encontrada"}

    return {
        "name": sessions[code]["name"],
        "admin": sessions[code]["admin"]
    }

@router.post("/session/leave")
def leave_session(data: JoinSessionRequest):

    leave_session_service(data.code, data.name)

    return {
        "message": "Saiu da sessão"
    }


@router.post("/session/reveal")
async def reveal_session(data: JoinSessionRequest):
    session = sessions.get(data.code)

    if not session:
        return {"error": "Sessão não encontrada"}

    if session["admin"] != data.name:
        return {"error": "Apenas o administrador pode revelar os votos"}

    reveal_votes(data.code)

    await manager.broadcast(
        data.code,
        json.dumps({
            "type": "state",
            "data": get_session_state(data.code)
        })
    )

    return {"message": "Votos revelados"}


@router.post("/session/reset")
async def reset_session(data: JoinSessionRequest):
    session = sessions.get(data.code)

    if not session:
        return {"error": "Sessão não encontrada"}

    if session["admin"] != data.name:
        return {"error": "Apenas o administrador pode reiniciar a votação"}

    reset_votes(data.code)

    await manager.broadcast(
        data.code,
        json.dumps({
            "type": "state",
            "data": get_session_state(data.code)
        })
    )

    return {"message": "Votação reiniciada"}


@router.post("/session/delete")
async def delete_session(data: JoinSessionRequest):
    result = delete_session_service(data.code, data.name)

    await manager.close_session(data.code)

    return result

# =========================
# WebSocket
# =========================

@router.websocket("/ws/{code}")
async def websocket_endpoint(websocket: WebSocket, code: str):

    print("Conectando ao WS...")

    if code not in sessions:
        await websocket.close()
        return

    await manager.connect(code, websocket)
    print("WS conectado com sucesso!")

    state = get_session_state(code)

    await websocket.send_text(json.dumps({
        "type": "state",
        "data": state
    }))

    try:
        while True:
            try:
                data = await websocket.receive_text()
            except:
                break
            try:
                message = json.loads(data)
            except:
                continue

            msg_type = message.get("type")
            user = message.get("user")

            if msg_type == "vote":

                value = message.get("value")

                if not user or not isinstance(value, int):
                    continue

                save_vote(code, user, value)

            elif msg_type == "reveal":
                if user == sessions[code]["admin"]:
                    reveal_votes(code)

            elif msg_type == "reset":
                if user == sessions[code]["admin"]:
                    reset_votes(code)

            elif msg_type == "sync":
                pass

            elif msg_type == "get_admin":
                await websocket.send_text(json.dumps({
                    "type": "admin",
                    "admin": sessions[code]["admin"]
                }))

                continue

            # =========================
            # BROADCAST DO ESTADO
            # =========================

            state = get_session_state(code)

            await manager.broadcast(
                code,
                json.dumps({
                    "type": "state",
                    "data": state
                })
            )

    except WebSocketDisconnect:
        print("WS desconectado")
        manager.disconnect(code, websocket)