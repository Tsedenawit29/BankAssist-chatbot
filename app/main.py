import streamlit as st
from chatbot import get_next_step
from db import save_user_data, is_duplicate_contact, init_db

# Initialize database tables
init_db()

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "step" not in st.session_state:
    st.session_state.step = "intent"
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# Configure page
st.set_page_config(
    page_title="BankAssist Chatbot",
    page_icon="🏦",
    layout="wide"
)

# Custom CSS for orange theme and better alignment
st.markdown("""
<style>
    /* Use Streamlit's default styling with orange accents */
    .stButton > button {
        background-color: #ff6600 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
    }
    .stButton > button:hover {
        background-color: #e55a00 !important;
    }
    
    /* Chat message styling */
    .user-message {
        background-color: #2d2d2d;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #ff6600;
    }
    .bot-message {
        background-color: #1a1a1a;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #0066cc;
    }
    
    /* Form alignment */
    .stForm {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🏦 BankAssist Chatbot")
st.markdown("**Your AI-powered banking assistant** 🤖")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <strong style="color: #ff6600;">You:</strong> {message['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
            <strong style="color: #0066cc;">BankAssist:</strong> {message['content']}
        </div>
        """, unsafe_allow_html=True)

# Welcome message if no messages
if not st.session_state.messages:
    st.info("👋 Hello! I'm BankAssist, your AI banking assistant. I can help you open a new bank account. Just tell me what you'd like to do!")
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hello! I'm BankAssist, your AI banking assistant. I can help you open a new bank account. Just tell me what you'd like to do!"})

# User input form with side-by-side alignment
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Type your message here...",
            key="user_input",
            placeholder="e.g., I want to open a savings account",
            label_visibility="collapsed"
        )
    with col2:
        submitted = st.form_submit_button("Send", use_container_width=True)

# Process user input only if form is submitted and input is non-empty
if submitted and st.session_state.user_input.strip():
    current_input = st.session_state.user_input.strip()
    user_message = {"role": "user", "content": current_input}
    st.session_state.messages.append(user_message)
    
    current_step = st.session_state.step
    user_data = st.session_state.user_data
    
    if current_step == "contact" and is_duplicate_contact(current_input):
        error_message = "⚠️ **Account Already Exists!** An account with this phone number or email address already exists. Please use a different phone number or email address to create a new account."
        bot_message = {"role": "assistant", "content": error_message}
        st.session_state.messages.append(bot_message)
        st.session_state.step = "contact"
    else:
        next_step, bot_response = get_next_step(current_input, current_step, user_data)
        
        bot_message = {"role": "assistant", "content": bot_response}
        st.session_state.messages.append(bot_message)
        
        if next_step == "submitted":
            try:
                if save_user_data(st.session_state.user_data):
                    followup_message = "\n\n💡 **Would you like to create another bank account?** Just let me know!"
                    followup_msg = {"role": "assistant", "content": followup_message}
                    st.session_state.messages.append(followup_msg)
                    st.session_state.step = "intent"
                    st.session_state.user_data = {}
            except Exception as e:
                error_message = f"❌ **Error Saving Data:** {str(e)}. Please try again or contact our support team."
                error_msg = {"role": "assistant", "content": error_message}
                st.session_state.messages.append(error_msg)
        else:
            st.session_state.step = next_step
            if current_step == "confirm" and next_step == "intent":
                st.session_state.user_data = {}
    
    st.rerun()

# The sidebar has been removed to simplify the app and align with the new data model.

# Footer
st.markdown("---")
st.markdown("**BankAssist Chatbot** - Making banking simple and accessible 🏦")