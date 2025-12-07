from db.database import get_user_state, save_user_state
from core.scheduler import is_available, save_appointment

async def step_handler(chat_id, nlp):
    state = get_user_state(chat_id)

    if state is None:
        state = {"step": "ASK_SERVICE"}
        save_user_state(chat_id, state)
        return "Olá! Qual serviço deseja? Corte, barba ou sobrancelha?"

    step = state["step"]

    # 1 — Perguntar serviço
    if step == "ASK_SERVICE":
        if not nlp["service"]:
            return "Qual serviço deseja? Corte, barba ou sobrancelha?"
        state["service"] = nlp["service"]
        state["step"] = "ASK_DATE"
        save_user_state(chat_id, state)
        return f"Perfeito! Para qual dia deseja marcar {nlp['service']}?"

    # 2 — Perguntar data
    if step == "ASK_DATE":
        if not nlp["date"]:
            return "Qual dia você gostaria? Pode falar 'sábado' ou 'amanhã'."
        state["date"] = nlp["date"]
        state["step"] = "ASK_TIME"
        save_user_state(chat_id, state)
        return "Beleza! E qual horário precisa?"

    # 3 — Perguntar horário
    if step == "ASK_TIME":
        if not nlp["time"]:
            return "Qual horário? Pode ser '9h', 'de manhã', etc."

        state["time"] = nlp["time"]

        # Validação do agendamento
        if not is_available(state):
            return "Esse horário não está disponível. Tente outro."

        save_appointment(state)
        save_user_state(chat_id, None)

        return f"Agendado! {state['service']} no dia {state['date']} às {state['time']}."

    return "Desculpe, não entendi. Vamos começar de novo."

