import streamlit as st

def init_session():
    if "step" not in st.session_state:
        st.session_state.step = "intent"
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
