from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Load the Gemini model you want to use
model = genai.GenerativeModel("model/gemini-2.0-flash")