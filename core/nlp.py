import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_message(text: str):
    prompt = f"""
    Interprete a frase e extraia os dados estruturados.
    Responda apenas JSON:
    - intent: agendar, cancelar, outro
    - service: corte, barba, sobrancelha ou vazio
    - date: data ISO ou vazio
    - time: horário HH:MM ou vazio
    - period: manhã, tarde, noite
    Frase: "{text}"
    """

    try:
        completion = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            response_format={"type": "json_schema"}
        )
        return completion.output_json
    except Exception as e:
        return {"intent": "", "service": "", "date": "", "time": "", "period": ""}

