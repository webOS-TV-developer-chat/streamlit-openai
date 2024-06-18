import streamlit as st
from utils import print_messages
from utils import img_to_html
from langchain_core.messages import ChatMessage
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from dotenv import load_dotenv
load_dotenv()


st.markdown(f"<H1>{img_to_html('img/iconchatbot.png',width=100)} AI CHATBOT</H1>", unsafe_allow_html=True)


if "messages" not in st.session_state:
  st.session_state["messages"] = []

print_messages()

if user_input := st.chat_input("input the message"):
    st.chat_message("user",avatar="img/iconuser.png").write(f"{user_input}")
    st.session_state["messages"].append(ChatMessage(role="user", content=user_input))
    
#use llm 
    prompt = ChatPromptTemplate.from_template("""Answer the question.
                                              {question}""")
    chain = prompt | ChatOpenAI(model="gpt-3.5-turbo") | StrOutputParser()
  #  chain = prompt | Ollama(model="llama2") | StrOutputParser()
    msg = chain.invoke({"question": user_input})   
    with st.chat_message("",avatar="img/iconchatbot.png",):
        st.write(msg)
#        st.markdown(f"<div align='right'>{msg}</div>", unsafe_allow_html=True)
        st.session_state["messages"].append(ChatMessage(role="assistant", content=msg))
