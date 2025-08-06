# 🏦 BankAssist Chatbot

An AI-powered banking assistant built with Streamlit that helps users open new bank accounts through a conversational interface.

## ✨ Features

### 🤖 **Simple Conversation Flow**
- Basic keyword-based conversation handling
- Step-by-step account opening form
- Multiple account types: Savings, Current, Business
- Input validation and error messages

### 🛡️ **Duplicate Prevention**
- Checks for existing phone/email before account creation
- Basic phone number format comparison
- Shows error message if duplicate found

### 💬 **Chat History**
- Saves conversations to local JSON file
- Previous chats shown in sidebar
- Click to reload past conversations
- Simple chat titles from first user message

### 🎨 **Simple UI**
- Streamlit interface with orange theme
- Black chat message backgrounds
- Input field with send button
- Basic responsive layout

### 💾 **Data Storage**
- ChromaDB for storing user account data
- JSON backup files as fallback
- Local data storage only
- Chat history saved between sessions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Tsedenawit29/BankAssist-chatbot.git
   cd BankAssist-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gemini API Key**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in the project root:
     ```bash
     GOOGLE_API_KEY=your_actual_api_key_here
     ```
   - Make sure `.env` is in your `.gitignore` file (for security)

4. **Run the application**
   ```bash
   streamlit run app/main.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start chatting with BankAssist! 🎉

### 🐳 Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:8501
```

## 📁 Project Structure

```
BankAssist-chatbot/
├── app/
│   ├── main.py          # Main Streamlit application
│   ├── chatbot.py       # Conversation logic and flow
│   ├── db.py            # Database operations (ChromaDB)
│   ├── state.py         # Session state and chat history
│   └── model.py         # AI model configuration
├── docker-compose.yml   # Docker configuration
├── Dockerfile          # Container setup
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## 🔧 How It Works

### Conversation Flow
1. **Intent Recognition** - User expresses desire to open account
2. **Account Type Selection** - Choose from Savings/Current/Business
3. **Information Collection** - Name, address, ID, contact details
4. **Confirmation** - Review and confirm all details
5. **Submission** - Save to database and provide next steps
6. **Follow-up** - Option to create additional accounts


```

### Data Persistence
- **ChromaDB**: Primary storage for user accounts
- **JSON Backup**: Fallback storage system
- **Chat History**: Local JSON file storage

## 🔒 Security & Privacy

- User data stored locally in ChromaDB
- No external API calls for sensitive data
- Chat history remains on user's machine
- Secure input validation and sanitization

## 🚀 Deployment

### Local Development
```bash
streamlit run app/main.py --server.port 8501
```

### Production with Docker
```bash
docker-compose up -d
```

### Cloud Deployment
- Compatible with Streamlit Cloud
- Heroku ready with Dockerfile
- AWS/GCP container deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Recent Updates

- ✅ **v2.0** - Added duplicate account prevention
- ✅ **v2.1** - Implemented chat history persistence
- ✅ **v2.2** - Updated to Streamlit default + orange theme
- ✅ **v2.3** - Enhanced form layout and UX
- ✅ **v2.4** - Fixed confirmation flow and follow-up prompts

**Tsedenawit** - [GitHub](https://github.com/Tsedenawit29)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- ChromaDB for efficient vector storage
- Open source community for inspiration

---
