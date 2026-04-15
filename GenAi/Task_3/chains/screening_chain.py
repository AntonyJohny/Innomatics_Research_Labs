import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from prompts.templates import screening_prompt

# Load environment variables from .env
load_dotenv()

def get_screening_chain():
    # Updated to a current supported model
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=0
    )
    
    chain = screening_prompt | llm
    return chain