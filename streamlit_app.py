import streamlit as st
from openai import OpenAI
from PIL import Image

# Secure API Key (replace only if necessary)
API_KEY = "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"

# Set up the app
st.set_page_config(page_title="SAP QM Expert Chatbot", layout="wide")
st.title("💬 SAP QM Expert Chatbot v3")
st.write(
    "This assistant combines OpenAI GPT-4 with real-world SAP QM knowledge from forums and experts.\n\n"
    "💡 You can upload or paste screenshots from SAP to help the bot assist you.\n"
    "🛠️ The bot will ask clarifying questions if your request is too broad."
)

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Upload or paste screenshot
uploaded_image = st.file_uploader("📷 Upload a screenshot from SAP (optional)", type=["png", "jpg", "jpeg"])

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "image" in message:
            st.image(message["image"], caption="User Screenshot")
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask a question about SAP Quality Management")

if prompt or uploaded_image:
    user_message = {"role": "user", "content": prompt}
    if uploaded_image:
        image = Image.open(uploaded_image)
        user_message["image"] = uploaded_image.getvalue()
        st.image(image, caption="User Screenshot")

    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        if uploaded_image:
            st.image(image, caption="User Screenshot")
        st.markdown(prompt or "*Screenshot only*")

    # Enriched system prompt
    system_prompt = (
        "You are a senior SAP Quality Management (QM) consultant with access to best practices from SAP Community, SAP Blogs, and SCN. "
        "Provide detailed, practical instructions, using transaction codes, integration tips, and real-world solutions. "
        "If the user question lacks details, ask follow-up questions to gather necessary context. "
        "Use screenshots when provided to validate UI-based issues or guide the user step-by-step. "
        "Focus on helping them configure, troubleshoot, or verify SAP QM processes with precision."
    )

    try:
        messages = [{"role": "system", "content": system_prompt}]

        if uploaded_image:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt or "Please analyze this screenshot."},
                    {"type": "image_url", "image_url": {"url": "data:image/png;base64," + uploaded_image.getvalue().decode("latin1")}}
                ]
            })
        else:
            messages.append({"role": "user", "content": prompt})

        response_stream = client.chat.completions.create(
            model="gpt-4-vision-preview" if uploaded_image else "gpt-4",
            messages=messages,
            stream=True,
            max_tokens=1500
        )

        with st.chat_message("assistant"):
            response = st.write_stream(response_stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Error: {e}")
