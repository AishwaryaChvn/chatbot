import streamlit as st
import streamlit.components.v1 as components

components.html(
    """
    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
        chat-title="Web-Search"
        agent-id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        language-code="en"></df-messenger>
    """,
    height=700, # try various values to see what works best (maybe use st.slider)
)
