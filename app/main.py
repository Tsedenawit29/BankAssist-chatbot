import streamlit as st
from chatbot import get_next_step
from db import save_user_data, user_exists
from model import model
from state import init_session

# Initialize session state
init_session()

# Custom CSS for dark theme with better visibility
st.markdown("""
<style>
    /* Dark theme */
    .main {
        background-color: #1a1a1a;
        color: white;
    }
    .stApp {
        background-color: #1a1a1a;
        color: white;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        color: white;
    }
    .user-message {
        background-color: #2d3748;
        border-left: 4px solid #ff6b35;
        color: white;
    }
    .bot-message {
        background-color: #2d3748;
        border-left: 4px solid #ff6b35;
        color: white;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
        background-color: #2d3748;
        color: white;
        border: 1px solid #ff6b35;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ff6b35;
        box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.2);
    }
    .stButton > button {
        border-radius: 20px;
        background-color: #ff6b35;
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background-color: #e55a2b;
    }
    .stMarkdown {
        color: white;
    }
    .stTitle {
        color: white;
    }
    .stHeader {
        color: white;
    }
    .stSidebar {
        background-color: #2d3748;
        color: white;
    }
    .stSidebar .stMarkdown {
        color: white;
    }
    /* Override Streamlit's default text colors */
    .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: white !important;
    }
    /* Welcome message styling */
    .welcome-message {
        background-color: #2d3748;
        border-left: 4px solid #ff6b35;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🏦 BankAssist Chatbot")
st.markdown("**Your AI-powered banking assistant** 🤖")

# Initialize chat history if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong style="color: #ff6b35;">You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong style="color: #ff6b35;">BankAssist:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)

# Welcome message (only show once)
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-message">
        <strong style="color: #ff6b35;">BankAssist:</strong> 👋 Hello! I'm BankAssist, your AI banking assistant. 
        I can help you open a new bank account. Just tell me what you'd like to do!
    </div>
    """, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hello! I'm BankAssist, your AI banking assistant. I can help you open a new bank account. Just tell me what you'd like to do!"})

# User input (form-based)
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "Type your message here...",
            key="user_input",
            placeholder="e.g., I want to open a savings account"
        )
    with col2:
        submitted = st.form_submit_button("Send")

# Process user input only if form is submitted and input is non-empty
if submitted and st.session_state.user_input.strip():
    current_input = st.session_state.user_input.strip()
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": current_input})
    current_step = st.session_state.step
    user_data = st.session_state.user_data
    # Check if user already exists (only for contact step)
    if current_step == "contact" and user_exists(current_input):
        bot_response = "⚠️ You've already submitted an application with this contact. Please use a different phone number or email."
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.session_state.step = "intent"  # Reset to start
    else:
        # Get next step and bot response
        next_step, bot_response = get_next_step(current_input, current_step, user_data)
        
        # Add bot response to chat first
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Handle submission
        if next_step == "submitted":
            try:
                # Save data to database
                save_user_data(user_data)
                # Add success confirmation message
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "✅ **Bank account application data saved successfully!** Your information has been securely stored in our system."
                })
                # Reset for new conversation after a brief delay
                st.session_state.step = "intent"
                st.session_state.user_data = {}
            except Exception as e:
                # Handle any database errors
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"❌ **Error saving data:** {str(e)}. Please try again or contact support."
                })
                # Don't reset on error, allow user to try again
        else:
            # Update session state for non-submission steps
            st.session_state.step = next_step
            # Clear user data if user said "no" to confirmation and we're restarting
            if current_step == "confirm" and next_step == "intent":
                st.session_state.user_data = {}
    # No need to clear st.session_state.user_input here; clear_on_submit handles it
    st.rerun()

# Sidebar with information
with st.sidebar:
    st.markdown("### 📋 Account Types")
    st.markdown("""
    - **Savings Account**: Earn interest on your money
    - **Current Account**: For daily transactions
    - **Business Account**: For business operations
    """)
    st.markdown("### 🔒 Security")
    st.markdown("Your information is encrypted and secure. We never share your personal data.")
    st.markdown("### 📞 Support")
    st.markdown("Need help? Contact our support team at support@bankassist.com")
    # Reset button
    if st.button("🔄 Start New Conversation"):
        st.session_state.messages = []
        st.session_state.step = "intent"
        st.session_state.user_data = {}
        st.session_state.user_input = ""
        st.rerun()

# Footer
st.markdown("---")
st.markdown("**BankAssist Chatbot** - Making banking simple and accessible 🏦")
