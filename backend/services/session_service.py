import random
import string
import os
from fastapi import HTTPException
from core.session_store import sessions

# =======================
# Gerar código único pra sessão
# =======================

def generate_code():
    while True:
        code = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=6
            )
        )

        if code not in sessions:
            return code

# =======================
# Configurações da sessão
# =======================

def create_session_service(session_name: str, admin_name: str):

    if not session_name or not session_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Nome da sessão obrigatório"
        )

    if not admin_name or not admin_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Nome do administrador obrigatório"
        )

    code = generate_code()

    sessions[code] = {
        "name": session_name,
        "admin": admin_name,
        "participants": [admin_name],
        "votes": {},
        "revealed": False
    }

    return {
        "code": code,
        "name": session_name,
        "admin": admin_name
    }

def join_session_service(code: str, name: str):
    if not code or not name or not name.strip():
        raise HTTPException(
            status_code=400,
            detail="Dados inválidos"
        )

    session = sessions.get(code)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Sessão não encontrada"
        )

    if name not in session["participants"]:
        session["participants"].append(name)

    print("Participantes:", session["participants"])

    return {
        "message": "Entrou na sessão"
    }


def get_session_state(code: str):
    session = sessions.get(code)

    if not session:
        return {
            "participants": [],
            "votes": {},
            "revealed": False,
            "admin": None,
            "name": ""
        }

    return {
        "participants": session["participants"],
        "votes": session["votes"],
        "revealed": session["revealed"],
        "admin": session["admin"],
        "name": session["name"]
    }

def leave_session_service(code: str, name: str):

    session = sessions.get(code)

    if not session:
        return

    if name in session["participants"]:
        session["participants"].remove(name)

    session["votes"].pop(name, None)

# =======================
# Configuração dos votos
# =======================

def save_vote(code: str, user: str, value: int):
    session = sessions.get(code)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Sessão não encontrada"
        )

    session["votes"][user] = value

    return {
        "message": "Voto registrado"
    }

def reveal_votes(code: str):
    session = sessions.get(code)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Sessão não encontrada"
        )

    session["revealed"] = True

    return {
        "message": "Votos revelados"
    }


def reset_votes(code: str):
    session = sessions.get(code)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Sessão não encontrada"
        )

    session["votes"] = {}
    session["revealed"] = False

    return {
        "message": "Votação reiniciada"
    }


def delete_session_service(code: str, name: str):
    session = sessions.get(code)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Sessão não encontrada"
        )

    if session["admin"] != name:
        raise HTTPException(
            status_code=403,
            detail="Apenas o administrador pode excluir a sessão"
        )

    del sessions[code]

    return {
        "message": "Sessão excluída"
    }


print("PROCESS ID:", os.getpid())