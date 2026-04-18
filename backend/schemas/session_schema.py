from pydantic import BaseModel

class CreateSessionRequest(BaseModel):
    name: str

class JoinSessionRequest(BaseModel):
    code: str
    name: str