from langchain_groq.chat_models import ChatGroq
from src.logger import logging
from src.exception import CustomException
from dotenv import load_dotenv
import sys
load_dotenv()

def get_llm():

    try:

        logging.info("Initializing LLM")

        llm = ChatGroq(
            model = "llama-3.1-8b-instant", 
            temperature = 0.1
        )

        logging.info("LLM initialized")

        return llm
    
    except Exception as e:

        raise CustomException(e, sys)
    