import streamlit as st
from typing import Generator
from groq import Groq
import os
from dotenv import load_dotenv
from utils import img_to_html

load_dotenv()
st.set_page_config(page_icon="img/iconchatbot.png", layout="wide",
                   page_title="ai chatbot")


st.markdown(f"<H1>{img_to_html('img/iconchatbot.png',width=80)} AI CHATBOT</H1>", unsafe_allow_html=True)
client = Groq(
    api_key=os.environ["GROQ_API_KEY"],
)

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# Define model details
models = {
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}

# Layout for model selection and max_tokens slider
col1, col2 = st.columns(2)

with col1:
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=1  # LLaMA3-70b
    )

# Detect model change and clear chat history if model has changed
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

max_tokens_range = models[model_option]["tokens"]

with col2:
    # Adjust max_tokens slider dynamically based on the selected model
    max_tokens = st.slider(
        "Max Tokens:",
        min_value=512,  # Minimum value to allow some flexibility
        max_value=max_tokens_range,
        # Default value or max allowed if less
        value=min(32768, max_tokens_range),
        step=512,
        help=f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: {max_tokens_range}"
    )

st.subheader("", divider="rainbow")
tabs_font_css = """
<style>
div[class*="stTextArea"] label p {
  font-size: 26px;
  color: black;
}

div[class*="stTextInput"] label p {
  font-size: 26px;
  color: blue;
}

div[class*="stNumberInput"] label p {
  font-size: 26px;
  color: green;
}
</style>
"""

st.write(tabs_font_css, unsafe_allow_html=True)

#st.text_area("Text area")
# st.text_input("Text input")
# st.number_input("Number input")



title = st.text_area("Welcome to AI Chatbot", 
                      "Hello, I am your AI Chatbot\n"
                      "I am here to help you. Ask me anything...")


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = 'img/iconchatbot.png' if message["role"] == "assistant" else 'img/iconuser.png'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content




if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='img/iconuser.png'):
        st.markdown(prompt)

    # Fetch response from Groq API
    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],
            max_tokens=max_tokens,
            stream=True
        )

        # Use the generator function with st.write_stream
        with st.chat_message("assistant", avatar="img/iconchatbot.png"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)
    except Exception as e:
        st.error(e, icon="🚨")

    # Append the full response to session_state.messages
    if isinstance(full_response, str):
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
    else:
        # Handle the case where full_response is not a string
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": combined_response})