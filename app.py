from fastapi import FastAPI
from telegram.webhook import router as telegram_router

app = FastAPI()

app.include_router(telegram_router)

@app.get("/")
def home():
    return {"status": "ok", "message": "Bot ativo!"}

