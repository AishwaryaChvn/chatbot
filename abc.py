import streamlit as st
import streamlit.components.v1 as components

st.header('Welcome to Food Delivery Service')
nav = st.sidebar.radio("MENU",["Pizza-100/-","Burger-150/-","Sandwich-100/-","Cutlet-150/-","Idli-80/-","Dosa-100/-"])
st.image('image.jpg')

components.html(
    """
    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
        chat-title="Web-Search"
        
        language-code="en"></df-messenger>
    """,
    height=700, # try various values to see what works best (maybe use st.slider)
)
