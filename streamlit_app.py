import streamlit as st
import os
from openai import OpenAI

# ─────────────────────────────────────────────
# 🔐 1. Cargar API Key desde secretos
# ─────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY no está configurada. Asegúrate de definirla en los 'Secrets'.")
    st.stop()

# 🔗 2. Configurar cliente de OpenAI para usar Groq
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# ─────────────────────────────────────────────
# 🧠 3. Prompt inicial del asistente experto SAP QM
# ─────────────────────────────────────────────
initial_system_prompt = {
    "role": "system",
    "content": """Eres un experto SAP QM con conocimiento profundo de SAP Community, SAP Blogs y SCN.
Explica todo con mucho detalle, como si estuvieras guiando a una persona sin experiencia previa en SAP.
Proporciona pasos detallados, transacciones relevantes, tips de configuración e integración con PP/MM/SD.
Utiliza las palabras de configuración y transacciones en inglés.
Incluye ejemplos reales, campos específicos que deben completarse y posibles errores comunes.
Haz preguntas aclaratorias si el usuario no ha sido específico."""
}

# ─────────────────────────────────────────────
# 🧼 4. UI y configuración general de la app
# ─────────────────────────────────────────────
st.set_page_config(page_title="SAP QM Chatbot", page_icon="🧠")
st.title("🧠 SAP QM Chatbot (Powered by Groq + LLaMA 3)")
st.write("Hazme preguntas sobre SAP Quality Management.")

# 🔁 Botón para reiniciar la conversación
if st.button("🧹 Nueva conversación"):
    st.session_state.chat_history = [initial_system_prompt]
    st.experimental_rerun()

# 🗃️ Inicializar historial de chat si no existe
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [initial_system_prompt]

# ─────────────────────────────────────────────
# 📜 5. Mostrar historial de conversación
# ─────────────────────────────────────────────
for msg in st.session_state.chat_history[1:]:  # omitimos el mensaje del system
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────
# ✍️ 6. Entrada del usuario + imagen opcional
# ─────────────────────────────────────────────
st.write("Puedes acompañar tu pregunta con una captura de pantalla.")

with st.form("user_input_form"):
    user_input = st.text_area("Pregunta:", placeholder="Describe tu duda o situación relacionada con SAP QM...")
    uploaded_file = st.file_uploader("📸 Sube una imagen si lo deseas:", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Enviar")

# Si el formulario se envía
if submitted:
    content = user_input.strip() if user_input else ""

    # Mostrar mensaje del usuario en el chat
    with st.chat_message("user"):
        if user_input:
            st.markdown(user_input)  # Mostrar texto
        if uploaded_file:
            st.image(uploaded_file, caption="Captura subida")  # Mostrar la imagen
            content += f"\n[Imagen subida: {uploaded_file.name}]"

    # Actualizar historial de la conversación
    st.session_state.chat_history.append({"role": "user", "content": content})

    # ─────────────────────────────────────────────
    # 🤖 7. Llamada al modelo y respuesta del bot
    # ─────────────────────────────────────────────
    with st.spinner("Pensando..."):
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.chat_history,
            temperature=0.7
        )
        bot_reply = response.choices[0].message.content

    # 💬 Mostrar respuesta del bot
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # Añadir la respuesta del bot al historial
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
