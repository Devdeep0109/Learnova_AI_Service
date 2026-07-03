from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.config import (
    LLM_MODEL,
    LLM_TEMPERATURE
)

load_dotenv()

llm = ChatGroq(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE
)