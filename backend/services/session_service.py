import random
import string

sessions = {}

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_session_service(name: str):
    code = generate_code()

    sessions[code] = {
        "name": name,
        "participants": [],
        "votes": {},
        "revealed": False
    }

    return {
        "code": code,
        "name": name
    }

def join_session_service(code: str, name: str):
    session = sessions.get(code)

    if not session:
        return {"error": "Sessão não encontrada"}

    session["participants"].append(name)

    return {"message": "Entrou na sessão"}