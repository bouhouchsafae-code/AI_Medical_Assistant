from fastapi import APIRouter

from pydantic import BaseModel

import ollama

import re

import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

# =========================
# 🚀 ROUTER
# =========================

router = APIRouter(

    prefix="/ai",

    tags=["AI Chat"]

)

# =========================
# 🧠 NLP MODEL
# =========================

nlp_model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

# =========================
# 🩺 MEDICAL CONTEXTS
# =========================

medical_examples = [

    "I am sick",
    "I have fever",
    "chest pain",
    "difficulty breathing",
    "pneumonia symptoms",
    "medical diagnosis",
    "xray analysis",
    "lung infection",
    "radiology report",
    "treatment for pneumonia",
    "patient disease",
    "respiratory illness",
    "doctor recommendation",
    "covid symptoms",
    "cough and fever",
    "heatmap explanation",
    "my lungs hurt",
    "I cannot breathe well",
    "I have chest infection",
    "I feel pain in my chest",
    "medical treatment",
    "hospital recommendation",
    "je suis malade",
"jai de la fievre",
"jai mal a la poitrine",
"je tousse",
"jai du mal a respirer",
"je me sens faible",
"jai une infection",
"jai besoin dun docteur",
"probleme respiratoire",
"symptomes de pneumonie",

]

# =========================
# 🔢 MEDICAL EMBEDDINGS
# =========================

medical_embeddings = nlp_model.encode(
    medical_examples
)

# =========================
# 📩 REQUEST
# =========================

class ChatRequest(BaseModel):

    message: str

# =========================
# 🧠 NLP MEDICAL FILTER
# =========================
def is_medical_question(message):

    # =========================
    # 🧹 CLEAN TEXT
    # =========================

    message = message.lower()

    cleaned_message = re.sub(
        r"[^a-zA-Z0-9\s]",
        "",
        message
    )

    # =========================
    # 🩺 DIRECT MEDICAL TERMS
    # =========================

    medical_terms = [

        "sick",
        "ill",
        "pain",
        "hurt",
        "hurts",
        "fever",
        "cough",
        "doctor",
        "hospital",
        "medicine",
        "treatment",
        "disease",
        "infection",
        "breathing",
        "lungs",
        "lung",
        "chest",
        "medical",
        "symptom",
        "symptoms",
        "xray",
        "x-ray",
        "radiology",
        "covid",
        "pneumonia"

    ]

    # =========================
    # ✅ DIRECT MATCH
    # =========================

    if any(

        term in cleaned_message

        for term in medical_terms

    ):

        return True

    # =========================
    # 🔢 NLP EMBEDDING
    # =========================

    message_embedding = nlp_model.encode(
        [cleaned_message]
    )

    similarities = cosine_similarity(

        message_embedding,

        medical_embeddings

    )[0]

    best_score = np.max(
        similarities
    )

    print(
        "Medical similarity score:",
        best_score
    )

    # =========================
    # ✅ THRESHOLD
    # =========================

    return best_score > 0.30
# =========================
# 💬 AI CHAT
# =========================

@router.post("/chat")
def chat(

    data: ChatRequest

):

    # =========================
    # ❌ NON MEDICAL FILTER
    # =========================

    if not is_medical_question(
        data.message
    ):

        return {

            "success": False,

            "response": (
                "I can only answer "
                "medical-related questions."
            )

        }

    # =========================
    # 🩺 SYSTEM PROMPT
    # =========================

    system_prompt = """

You are an advanced medical AI assistant.

Your role is ONLY to answer
medical-related questions.

You specialize in:

- radiology
- pneumonia
- chest xray
- lung diseases
- respiratory diseases
- treatments
- symptoms
- diagnosis
- heatmaps
- medical recommendations

IMPORTANT RULES:

1. ONLY answer medical-related questions.

2. If the user asks a non-medical question,
politely refuse.

3. ALWAYS answer in the SAME LANGUAGE
used by the user.

- If the user writes in French,
respond in French.

- If the user writes in English,
respond in English.

4. Keep responses professional,
clear, concise, and medically accurate.

"""

    # =========================
    # 🤖 OLLAMA RESPONSE
    # =========================

    response = ollama.chat(

        model="mistral",

        messages=[

            {

                "role": "system",

                "content": system_prompt

            },

            {

                "role": "user",

                "content": data.message

            }

        ]

    )

    # =========================
    # ✅ RETURN
    # =========================

    return {

        "success": True,

        "response":
            response["message"]["content"]

    }