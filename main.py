import streamlit as st
from utils import print_messages
from langchain_core.messages import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Chatbot", page_icon="")
st.title("Chatbot")

if "messages" not in st.session_state:
  st.session_state["messages"] = []

print_messages()

if user_input := st.chat_input("input the message"):
    st.chat_message("user").write(f"{user_input}")
    st.session_state["messages"].append(ChatMessage(role="user", content=user_input))
    
#use llm 
    prompt = ChatPromptTemplate.from_template("""Answer the question.
                                              {question}""")
    chain = prompt | ChatOpenAI(model="gpt-3.5-turbo") | StrOutputParser()
    msg = chain.invoke({"question": user_input})
    with st.chat_message("assistant"):
        st.write(msg)
        st.session_state["messages"].append(ChatMessage(role="assistant", content=msg))
