import streamlit as st
import json
import os
from datetime import datetime

def init_session():
    if "step" not in st.session_state:
        st.session_state.step = "intent"
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = load_chat_history()
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None

def load_chat_history():
    """Load chat history from file"""
    try:
        if os.path.exists("./chat_history.json"):
            with open("./chat_history.json", 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading chat history: {e}")
        return []

def save_chat_history():
    """Save current chat conversation to history"""
    try:
        if st.session_state.messages and len(st.session_state.messages) > 1:  # Only save if there are actual conversations
            chat_data = {
                "id": st.session_state.current_chat_id or datetime.now().strftime("%Y%m%d_%H%M%S"),
                "timestamp": datetime.now().isoformat(),
                "messages": st.session_state.messages.copy(),
                "title": generate_chat_title(st.session_state.messages)
            }
            
            # Update existing chat or add new one
            chat_exists = False
            for i, chat in enumerate(st.session_state.chat_history):
                if chat["id"] == chat_data["id"]:
                    st.session_state.chat_history[i] = chat_data
                    chat_exists = True
                    break
            
            if not chat_exists:
                st.session_state.chat_history.insert(0, chat_data)  # Add to beginning
            
            # Keep only last 20 chats
            st.session_state.chat_history = st.session_state.chat_history[:20]
            
            # Save to file
            with open("./chat_history.json", 'w') as f:
                json.dump(st.session_state.chat_history, f, indent=2)
                
    except Exception as e:
        print(f"Error saving chat history: {e}")

def generate_chat_title(messages):
    """Generate a title for the chat based on the first user message"""
    for message in messages:
        if message["role"] == "user":
            content = message["content"][:40]  # First 40 characters
            if len(message["content"]) > 40:
                content += "..."
            return content
    return "New Chat"

def load_chat(chat_id):
    """Load a specific chat by ID"""
    for chat in st.session_state.chat_history:
        if chat["id"] == chat_id:
            st.session_state.messages = chat["messages"].copy()
            st.session_state.current_chat_id = chat_id
            # Reset other states for loaded chat
            st.session_state.step = "intent"
            st.session_state.user_data = {}
            return True
    return False

def start_new_chat():
    """Start a new chat session"""
    # Save current chat if it has messages
    if st.session_state.messages:
        save_chat_history()
    
    # Reset session for new chat
    st.session_state.messages = []
    st.session_state.step = "intent"
    st.session_state.user_data = {}
    st.session_state.current_chat_id = None

def clear_all_history():
    """Clear all message history"""
    try:
        st.session_state.chat_history = []
        # Remove the history file
        import os
        if os.path.exists("./chat_history.json"):
            os.remove("./chat_history.json")
        return True
    except Exception as e:
        print(f"Error clearing history: {e}")
        return False
