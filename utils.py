import streamlit as st
import base64
from pathlib import Path

def print_messages():
  if "messages" in st.session_state and len(st.session_state["messages"]) > 0:
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
def img_to_html(img_path, width=None):
    if width:
        img_html = "<img src='data:image/png;base64,{}' style='width: {}px' class='img-fluid'>".format(
          img_to_bytes(img_path),
          width
        )
    else:
        img_html = "<img src='data:image/png;base64,{}' style='width: ' class='img-fluid'>".format(
          img_to_bytes(img_path)
    )
    return img_html