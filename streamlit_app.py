import streamlit as st
import os
from openai import OpenAI  # Groq usa la misma clase del SDK de OpenAI

# Obtiene la clave desde las variables de entorno
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Asegúrate de que la variable esté presente
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY no está configurada. Asegúrate de definirla.")
    st.stop()

# Cliente de Groq (OpenAI-compatible)
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"  # Muy importante
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
            model="mistral-7b-8k",  # Puedes cambiarlo por "mixtral-8x7b-32768" si quieres uno más potente
            messages=[
                {"role": "system", "content": "Eres un experto en SAP Quality Management. Responde de forma clara y profesional."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        st.success(response.choices[0].message.content)
