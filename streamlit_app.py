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

# Configuración inicial de la página
st.set_page_config(page_title="SAP QM Chatbot", page_icon="🧠")
st.title("🧠 SAP QM Chatbot (Powered by Groq + LLaMA 3)")
st.write("Hazme preguntas sobre SAP Quality Management.")

# Inicializa el historial de mensajes en session_state si no existe
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "Eres un experto en SAP Quality Management. Responde de forma clara y profesional."}
    ]

# Mostrar historial en pantalla
for message in st.session_state.chat_history[1:]:  # omitimos el mensaje del sistema
    if message["role"] == "user":
        st.markdown(f"**Tú:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")

# Entrada del usuario
user_input = st.text_input("Pregunta:", key="user_input")

if user_input:
    # Agrega mensaje del usuario al historial
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Pensando..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # o "mistral-7b-8k"
            messages=st.session_state.chat_history,
            temperature=0.7
        )
        bot_reply = response.choices[0].message.content

    # Agrega respuesta del bot al historial
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

    # Limpiar campo de texto
    st.rerun()
