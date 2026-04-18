from fastapi import FastAPI
from routers.session_router import router as session_router

app = FastAPI()

app.include_router(session_router)

@app.get("/")
def root():
    return {"message": "PokerUFF backend rodando"}