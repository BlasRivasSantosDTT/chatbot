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

# Prompt inicial del sistema (lo guardamos como variable)
initial_system_prompt = {
    "role": "system",
    "content": """Eres un experto SAP QM con conocimiento profundo de SAP Community, SAP Blogs y SCN.
Explica todo con mucho detalle, como si estuvieras guiando a una persona sin experiencia previa en SAP.
Proporciona pasos detallados, transacciones relevantes, tips de configuración e integración con PP/MM/SD.
Utiliza las palabras de configuración y transacciones en inglés.
Incluye ejemplos reales, campos específicos que deben completarse y posibles errores comunes.
Haz preguntas aclaratorias si el usuario no ha sido específico."""
}

# Configuración de la app
st.set_page_config(page_title="SAP QM Chatbot", page_icon="🧠")
st.title("🧠 SAP QM Chatbot (Powered by Groq + LLaMA 3)")
st.write("Hazme preguntas sobre SAP Quality Management.")

# Botón para reiniciar la conversación
if st.button("🧹 Nueva conversación"):
    st.session_state.chat_history = [initial_system_prompt]
    st.rerun()

# Inicializar historial de chat si no existe
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [initial_system_prompt]

# Mostrar historial
for msg in st.session_state.chat_history[1:]:  # omitimos el mensaje del system
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
user_input = st.chat_input("Escribe tu pregunta aquí...")
uploaded_file = st.file_uploader("📸 Sube una captura de pantalla (opcional)", type=["png", "jpg", "jpeg"])

if user_input or uploaded_file:
    content = user_input if user_input else ""

    if uploaded_file:
        with st.chat_message("user"):
            if user_input:
                st.markdown(user_input)
            st.image(uploaded_file, caption="Captura subida")
        content += f"\n[El usuario ha subido una imagen: {uploaded_file.name}]"
    else:
        with st.chat_message("user"):
            st.markdown(user_input)

    st.session_state.chat_history.append({"role": "user", "content": content})

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
