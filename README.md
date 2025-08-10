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
- Validates phone and email format
- Shows error message if a duplicate contact or invalid format is found

### 💬 **New Chat Feature**
- A **"New Chat" button** allows users to reset the conversation and start over at any time, providing a clear and simple user experience.

### 🎨 **Simple UI**
- Streamlit interface with an orange theme
- Black chat message backgrounds
- Input field with send button
- Basic responsive layout

### 💾 **Data Storage**
- **PostgreSQL** or **SQLite** for storing user application data
- The application stores submitted user details in a relational database for bank employee follow-up.
- A single `account_applications` table is used to store user information and application status.

***

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker
- Docker Compose

### Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Tsedenawit29/BankAssist-chatbot.git](https://github.com/Tsedenawit29/BankAssist-chatbot.git)
   cd BankAssist-chatbot
````

2.  **Set up Gemini API Key and Database URL**

      - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
      - Create a `.env` file in the project root:
        ```bash
        GOOGLE_API_KEY=your_actual_api_key_here
        # This URL is for local development without Docker Compose
        # DATABASE_URL=sqlite:///bank_applications.db
        ```
      - Make sure `.env` is in your `.gitignore` file (for security)

3.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

### 🐳 Docker Setup (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:8501
```

This will automatically create and start both the PostgreSQL database container and the Streamlit chatbot container.

-----

## 📁 Project Structure

```
BankAssist-chatbot/
├── app/
│   ├── main.py          # Main Streamlit application
│   ├── chatbot.py       # Conversation logic and flow
│   ├── db.py            # Database operations (SQLAlchemy)
│   └── utils.py         # Helper functions for input validation
├── docker-compose.yml   # Docker configuration for multi-container setup
├── Dockerfile          # Container setup
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

-----

## 🔧 How It Works

### Conversation Flow

1.  **Intent Recognition** - User expresses desire to open an account.
2.  **Account Type Selection** - User chooses from Savings, Current, or Business.
3.  **Information Collection** - The chatbot collects the user's name, address, ID, and contact details.
4.  **Input Validation** - The contact information is validated for correct format (email or phone).
5.  **Confirmation** - The user reviews and confirms all details.
6.  **Submission** - The application data is saved to the PostgreSQL database.
7.  **Follow-up** - A confirmation message is sent, and the user is informed that a bank employee will contact them.

### Data Persistence

  - The chatbot uses **SQLAlchemy** to connect to a **PostgreSQL** database.
  - A single table, `account_applications`, stores each user's submitted data.
  - **Data Types:** The schema uses the flexible `Text` data type for fields like `full_name` and `address`, ensuring that all variable-length text data is stored completely without risk of truncation.
  - This approach ensures data is persistent, structured, and easily accessible for a bank's back-end systems or employees for follow-up.
  - Unlike the previous version, this system does not store conversation history, focusing solely on the key application data.

-----

## 🔒 Security & Privacy

  - User data is stored in a private PostgreSQL database.
  - The chatbot performs secure input validation.
  - All sensitive data is handled locally within the Dockerized environment and not sent to external APIs.

-----

## 🚀 Deployment

### Local Development

```bash
# Set DATABASE_URL if you want to use PostgreSQL on your local machine
streamlit run app/main.py --server.port 8501
```

### Production with Docker

```bash
docker-compose up -d
```

### Cloud Deployment

  - The Dockerized setup is ideal for container deployment on platforms like AWS, GCP, or Azure.

-----

## 🤝 Contributing

1.  Fork the repository
2.  Create a feature branch (`git checkout -b feature/amazing-feature`)
3.  Commit your changes (`git commit -m 'Add amazing feature'`)
4.  Push to the branch (`git push origin feature/amazing-feature`)
5.  Open a Pull Request

