from db.database import save_appointment_db

def is_available(state):
    # Aqui você valida conflito de horário.
    # Por enquanto, vamos aceitar tudo.
    return True

def save_appointment(state):
    save_appointment_db(state)

