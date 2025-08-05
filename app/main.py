import streamlit as st
from app.chatbot import get_next_step
from app.db import save_user_data, user_exists
from app.model import model
from app.state import init_session

# Initialize session state
init_session()

st.title("🏦 Bank Account Opening Assistant")

st.markdown("Welcome to **BankBot** 👋\nAsk me to open an account and I'll guide you through it!")

with st.expander("📌 How It Works"):
    st.markdown("""
    - Type your request (e.g. _\"I want to open a savings account\"_)
    - I'll ask a few simple questions
    - Your info will be submitted securely
    """)

# User input
user_input = st.text_input("You:", key="input")

if user_input:
    current_step = st.session_state.step
    user_data = st.session_state.user_data

    if current_step == "contact" and user_exists(user_input):
        st.markdown("⚠️ You've already submitted an application with this contact.")
        st.stop()

    next_step, bot_response = get_next_step(user_input, current_step, user_data)

    st.session_state.step = next_step

    if next_step == "submitted":
        save_user_data(user_data)

    st.markdown(f"**BankBot:** {bot_response}")
