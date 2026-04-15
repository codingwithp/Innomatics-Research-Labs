import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_llm(temperature=0.3):
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=temperature
    )