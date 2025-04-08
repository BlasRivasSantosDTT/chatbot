import streamlit as st
from transformers import pipeline

# Carga el modelo de Hugging Face
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2", device_map="auto")

model = load_model()

st.title("🧠 SAP QM Chatbot (Gratis con Mistral)")
st.write(
    "Este chatbot usa un modelo open-source de alto rendimiento para ayudarte con SAP Quality Management, "
    "basado en conocimientos reales de comunidades SAP."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostrar mensajes anteriores
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de usuario
prompt = st.chat_input("Pregunta sobre SAP QM")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    system_prompt = (
        "Eres un experto SAP QM con conocimiento profundo de SAP Community, SAP Blogs y SCN. "
        "Proporciona pasos detallados, transacciones relevantes, tips de configuración e integración con PP/MM/SD. "
        "Haz preguntas aclaratorias si el usuario no ha sido específico. "
        "Usuario pregunta: " + prompt
    )

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = model(system_prompt, max_new_tokens=512, do_sample=True, temperature=0.7)[0]["generated_text"]
            response_text = response[len(system_prompt):].strip()
            st.markdown(response_text)
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
