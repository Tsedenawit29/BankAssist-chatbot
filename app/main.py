import streamlit as st
from chatbot import get_next_step
from db import save_user_data, is_duplicate_contact
from model import model
from state import init_session, save_chat_history, generate_chat_title, load_chat, start_new_chat, clear_all_history

# Initialize session state
init_session()

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
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
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
    col1, col2 = st.columns([5, 1])  # Adjusted ratio for better alignment
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
    # Add user message to chat
    user_message = {"role": "user", "content": current_input}
    st.session_state.messages.append(user_message)
    
    current_step = st.session_state.step
    user_data = st.session_state.user_data
    
    # Check for duplicate contact information (only for contact step)
    if current_step == "contact" and is_duplicate_contact(current_input):
        error_message = "⚠️ **Account Already Exists!** An account with this phone number or email address already exists. Please use a different phone number or email address to create a new account."
        bot_message = {"role": "assistant", "content": error_message}
        st.session_state.messages.append(bot_message)
        st.session_state.step = "contact"  # Stay on contact step to allow retry
    else:
        # Get next step and bot response
        next_step, bot_response = get_next_step(current_input, current_step, user_data)
        
        # Add bot response to chat
        bot_message = {"role": "assistant", "content": bot_response}
        st.session_state.messages.append(bot_message)
        
        # Handle submission
        if next_step == "submitted":
            try:
                # Save data to database
                if save_user_data(user_data):
                    # The bot response already contains the success message and next steps
                    # Just add a follow-up message asking about creating another account
                    followup_message = "\n\n💡 **Would you like to create another bank account?** Just let me know!"
                    followup_msg = {"role": "assistant", "content": followup_message}
                    st.session_state.messages.append(followup_msg)
                    # Save completed conversation to history
                    save_chat_history()
                    # Reset for new conversation but keep chat active
                    st.session_state.step = "intent"
                    st.session_state.user_data = {}
            except Exception as e:
                # Handle any database errors
                error_message = f"❌ **Error Saving Data:** {str(e)}. Please try again or contact our support team."
                error_msg = {"role": "assistant", "content": error_message}
                st.session_state.messages.append(error_msg)
                # Don't reset on error, allow user to try again
        else:
            # Update session state for non-submission steps
            st.session_state.step = next_step
            # Clear user data if user said "no" to confirmation and we're restarting
            if current_step == "confirm" and next_step == "intent":
                st.session_state.user_data = {}
    
    st.rerun()

# Sidebar with chat history and controls
with st.sidebar:
    st.markdown("### 🏦 BankAssist")
    
    # New chat button
    if st.button("➕ New Chat", use_container_width=True):
        start_new_chat()
        st.rerun()
    
    st.markdown("---")
    
    # Chat History
    st.markdown("### 💬 Chat History")
    
    if st.session_state.chat_history:
        for i, chat in enumerate(st.session_state.chat_history[:10]):  # Show last 10 chats
            chat_title = chat.get("title", "New Chat")
            if len(chat_title) > 35:
                chat_title = chat_title[:35] + "..."
            
            # Format timestamp
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(chat.get("timestamp", ""))
                time_str = dt.strftime("%m/%d %H:%M")
            except:
                time_str = ""
            
            # Highlight current chat
            if st.session_state.current_chat_id == chat["id"]:
                st.markdown(f"🔸 **{chat_title}**")
                if time_str:
                    st.markdown(f"*{time_str}*")
            else:
                if st.button(f"💬 {chat_title}", key=f"chat_{i}", use_container_width=True):
                    load_chat(chat["id"])
                    st.rerun()
                if time_str:
                    st.markdown(f"*{time_str}*")
            
            st.markdown("---")
    else:
        st.markdown("*No chat history yet*")
    
    # Current session info
    if st.session_state.messages:
        st.markdown("### 📊 Current Session")
        st.markdown(f"**Messages:** {len(st.session_state.messages)}")
        st.markdown(f"**Step:** {st.session_state.step.title()}")
        st.markdown("---")
    
    # Clear all history button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear All History", use_container_width=True):
            if clear_all_history():
                st.success("Chat history cleared!")
            st.rerun()

# Footer
st.markdown("---")
st.markdown("**BankAssist Chatbot** - Making banking simple and accessible 🏦")
