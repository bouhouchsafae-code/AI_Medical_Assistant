import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

# =========================
# 🧠 AI MEDICAL FILTER
# =========================

def is_medical_question(question):

    filter_prompt = f"""
You are a strict classifier.

Your job is to determine whether the user's question is related to:
- medicine
- healthcare
- radiology
- symptoms
- diseases
- treatments
- hospitals
- lungs
- pneumonia
- health

Rules:
- Reply ONLY with YES or NO.
- YES = medical question
- NO = non-medical question

Question:
{question}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": filter_prompt,
            "stream": False
        }
    )

    result = response.json()["response"].strip().upper()

    return "YES" in result

# =========================
# 🤖 MAIN CHATBOT
# =========================

def medical_chatbot(question, context=""):

    # =========================
    # 🔒 FILTER
    # =========================

    if not is_medical_question(question):

        return (
            "⚠️ I can only answer medical and healthcare-related questions."
        )

    # =========================
    # 🧠 MEDICAL PROMPT
    # =========================

    prompt = f"""
You are an advanced AI medical assistant specialized in pneumonia detection and healthcare.

Medical Context:
{context}

User Question:
{question}

Instructions:
- Give professional medical answers.
- Be clear and medically accurate.
- Stay focused on healthcare and medicine only.

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        return response.json()["response"]

    return "Error contacting AI model."