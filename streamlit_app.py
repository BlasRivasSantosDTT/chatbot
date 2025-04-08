import streamlit as st
import os
from openai import OpenAI

# Cargar API Key de los secretos de Streamlit
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY no está configurada. Asegúrate de definirla en los 'Secrets'.")
    st.stop()

# Cliente OpenAI apuntando a Groq
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Configuración de la app
st.set_page_config(page_title="SAP QM Chatbot", page_icon="🧠")
st.title("🧠 SAP QM Chatbot (Powered by Groq + LLaMA 3)")
st.write("Hazme preguntas sobre SAP Quality Management.")

# Inicializar historial de chat si no existe
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "Eres un experto SAP QM con conocimiento profundo de SAP Community, SAP Blogs y SCN.
        Proporciona pasos detallados, transacciones relevantes, tips de configuración e integración con PP/MM/SD., especificando muy en detalle los pasos qué seguir, qué campos cubrir, ...
        Haz preguntas aclaratorias si el usuario no ha sido específico."}
    ]

# Mostrar historial
for msg in st.session_state.chat_history[1:]:  # omitimos el mensaje del system
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
user_input = st.chat_input("Escribe tu pregunta aquí...")

if user_input:
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Generar respuesta
    with st.spinner("Pensando..."):
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.chat_history,
            temperature=0.7
        )
        bot_reply = response.choices[0].message.content

    # Mostrar respuesta del bot
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

if st.button("🧹 Nueva conversación"):
    st.session_state.chat_history = [
        {"role": "system", "content": "Eres un experto en SAP Quality Management. Responde de forma clara y profesional."}
    ]
    st.rerun()
