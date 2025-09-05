from flask import Flask, request, jsonify, render_template
import os
import requests
import imaplib
import email
from datetime import datetime

app = Flask(__name__, static_url_path='/static', static_folder='static')


def get_emails():
    # Conexión con Gmail
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))

    # Seleccionar bandeja de entrada
    imap.select("INBOX")

    # Fecha de hoy en formato IMAP
    today = datetime.today().strftime("%d-%b-%Y")

    # Buscar los correos de hoy
    status, messages = imap.search(None, f'(SINCE "{today}")')
    email_ids = messages[0].split()

    contenedor = []
    for emails in email_ids:
        status, msg_data = imap.fetch(emails, "(RFC822)")
        raw_msg = msg_data[0][1]
        msg = email.message_from_bytes(raw_msg)
        contenedor.append(msg)

    contenedor_con_todo = []
    body = ""
    for msg in contenedor:
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                    body += part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")
        contenedor_con_todo.append(body)

    imap.close()
    imap.logout()
    return contenedor_con_todo

@app.route('/')
def index():
    """Serves the chat web interface"""
    return render_template('index.html')

@app.route("/api/chat")
def chat():
    contenedor = get_emails()
    contenedor_final = []
    # Leer el prompt del sistema desde archivo externo
    with open(os.path.join(os.path.dirname(__file__), "system_prompt.txt"), encoding="utf-8") as f:
        system_prompt = f.read()
    for prompt in contenedor:
        try:
            chat_request = {
                "model": os.getenv("LLM_MODEL_NAME"),
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                os.getenv("LLM_BASE_URL"),
                headers=headers,
                json=chat_request,
                timeout=60
            )
            if response.status_code != 200:
                return jsonify({
                    "error": f"LLM returned {response.status_code}: {response.text}"
                }), 500
            chat_response = response.json()
            if chat_response.get("choices") and len(chat_response["choices"]) > 0:
                model_text = chat_response["choices"][0]["message"]["content"].strip()
            else:
                model_text = ""
            contenedor_final.append({"response": model_text})
        except Exception as e:
            contenedor_final.append({"error": str(e)})
    return jsonify(contenedor_final)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
