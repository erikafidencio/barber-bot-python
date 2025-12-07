from fastapi import APIRouter, Request
from core.state import step_handler
from core.nlp import parse_message
from utils.logger import log

router = APIRouter()

@router.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    log("Recebido:", data)

    try:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
    except:
        return {"ok": True}

    # NLP
    nlp = parse_message(text)

    # FSM
    response = await step_handler(chat_id, nlp)

    # Telegram response format
    return {
        "method": "sendMessage",
        "chat_id": chat_id,
        "text": response
    }

