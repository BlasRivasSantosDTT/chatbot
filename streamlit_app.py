import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 SAP QM Expert Chatbot")
st.write(
    "Welcome to the SAP QM Expert Chatbot! This chatbot utilizes OpenAI's GPT model to provide insights related to SAP Quality Management."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field for user input.
    if prompt := st.chat_input("Ask a question about SAP Quality Management:"):

        # Store and display the user prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare a context-rich prompt for the OpenAI API to generate better responses.
        enriched_prompt = (
            "You are an expert in SAP Quality Management (QM). "
            "Provide comprehensive answers to questions related to quality processes, "
            "inspection methodologies, quality notifications, quality planning, and integration with other SAP modules. "
            "User Query: " + prompt
        )

        # Generate a response using the OpenAI API.
        try:
            stream = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": enriched_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
            )

            # Stream the response to the chat and append to session state.
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error("An error occurred while generating the response: " + str(e))
