import streamlit as st
from streamlit_chat import message

placeholder = st.empty()
input_ = st.text_input("you:")
message_history.append(input_)

with placeholder.container():
    for message_ in message_history:
        message(message_)
