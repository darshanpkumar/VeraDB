import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the variables from your local hidden .env file
load_dotenv()

# 2. Securely extract the key from system environment properties
API_KEY = os.getenv("GEMINI_API_KEY")

# 3. Pass the hidden variable key to the configuration layer
genai.configure(api_key=API_KEY)

# Initialize the Gemini Flash model instance
model = genai.GenerativeModel("gemini-2.5-flash")

def ask_llm(question: str, context: str) -> str:
    """
    Stitches the structured context chunk and the user query together 
    into a prompt instruction template and sends it to the LLM.
    """
    prompt = f"""
Context:
{context}

Question:
{question}

Answer only using the context.
"""
    response = model.generate_content(prompt)
    return response.text