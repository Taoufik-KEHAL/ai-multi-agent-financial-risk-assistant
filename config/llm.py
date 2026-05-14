from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def obtenir_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )
