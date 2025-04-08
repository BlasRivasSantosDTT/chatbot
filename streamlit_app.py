import streamlit as st
import os
from openai import OpenAI

# Obtén la clave de API de los secretos de Streamlit
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY no está configurada. Asegúrate de definirla en los 'Secrets'.")
    st.stop()

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

if user_input:
    with st.spinner("Pensando..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Eres un experto en SAP Quality Management. Responde de forma clara y profesional."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        st.success(response.choices[0].message.content)
