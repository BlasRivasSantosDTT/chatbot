import streamlit as st
from openai import OpenAI
from PIL import Image
import base64

# Hardcoded API key (used securely in production scenarios)
API_KEY = "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"

st.set_page_config(page_title="SAP QM Expert Chatbot", layout="wide")
st.title("💬 SAP QM Expert Chatbot v4")
st.write(
    "This chatbot uses GPT-4.5 and expert-level SAP QM knowledge from real SAP communities (SCN, SAP Blogs, etc.).\n\n"
    "🔍 Upload screenshots or files if needed. The assistant can analyze visual content to guide your troubleshooting.\n"
    "📌 It will ask you clarifying questions when your input is not specific enough for an accurate response."
)

# OpenAI client
client = OpenAI(api_key=API_KEY)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "image" in message:
            st.image(message["image"], caption="Uploaded Screenshot")
        if "file_name" in message:
            st.markdown(f"📎 **File uploaded:** {message['file_name']}")
        st.markdown(message["content"])

# Inputs
uploaded_image = st.file_uploader("📷 Upload a screenshot (optional)", type=["png", "jpg", "jpeg"])
uploaded_file = st.file_uploader("📄 Upload a file (optional)", type=["pdf", "docx", "txt"])
prompt = st.chat_input("Ask a question about SAP Quality Management")

# Process user input
if prompt or uploaded_image or uploaded_file:
    user_message = {"role": "user", "content": prompt or "*No text question provided*"}

    # If screenshot uploaded
    if uploaded_image:
        image_bytes = uploaded_image.read()
        user_message["image"] = image_bytes
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # If file uploaded
    if uploaded_file:
        file_content = uploaded_file.read()
        file_text = file_content.decode("utf-8", errors="ignore")[:1000]  # show only beginning
        user_message["file_name"] = uploaded_file.name
        prompt += f"\n\n(File excerpt for context):\n{file_text}"

    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        if uploaded_image:
            st.image(image_bytes, caption="User Screenshot")
        if uploaded_file:
            st.markdown(f"📎 **File uploaded:** {uploaded_file.name}")
        st.markdown(prompt or "*Screenshot only*")

    # Enriched system prompt
    system_prompt = (
        "You are a highly experienced SAP Quality Management (QM) consultant with access to real-world knowledge from SAP Community, SAP Blogs, and SCN. "
        "When answering, always consider T-Codes, configurations, integrations with PP/MM/SD, inspection lot logic, and notifications. "
        "Ask clarifying questions if the user's request is too vague or lacks detail. "
        "If screenshots are included, visually analyze the UI and guide step-by-step. "
        "If files are uploaded, extract key details and respond accordingly. "
        "Your goal is to help the user precisely configure, troubleshoot, or verify SAP QM systems."
    )

    try:
        # Compose OpenAI API call
        messages = [{"role": "system", "content": system_prompt}]

        if uploaded_image:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt or "Please analyze this screenshot."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                ]
            })
            model = "gpt-4-vision-preview"
        else:
            messages.append({"role": "user", "content": prompt})
            model = "gpt-4.5-preview"

        response_stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            max_tokens=1500
        )

        with st.chat_message("assistant"):
            response = st.write_stream(response_stream)

        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"❌ Error: {e}")
