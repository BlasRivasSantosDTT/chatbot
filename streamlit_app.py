import streamlit as st
import os
from openai import OpenAI

# Usa tu clave de API de Groq aquí
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "TU_API_KEY_AQUI")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Interfaz de Streamlit
st.set_page_config(page_title="SAP QM Chatbot", page_icon="🧠")
st.title("🧠 SAP QM Chatbot (Powered by Groq + Mistral)")
st.write("Hazme preguntas sobre SAP Quality Management.")

# Entrada del usuario
user_input = st.text_input("Pregunta:")

# Cuando el usuario escribe algo
if user_input:
    with st.spinner("Pensando..."):
        response = client.chat.completions.create(
            model="mistral-7b-8k",
            messages=[
                {"role": "system", "content": "Eres un experto en SAP Quality Management. Responde de forma clara y profesional."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        st.success(response.choices[0].message.content)
