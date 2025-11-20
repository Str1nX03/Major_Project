from langchain_groq.chat_models import ChatGroq
from src.logger import logging
from src.exception import CustomException
import sys
import os

def get_llm():

    if os.getenv("GROQ_API_KEY") is None:

        raise Exception("GROQ_API_KEY is not set")

    try:

        logging.info("Initializing LLM")

        llm = ChatGroq(
            model = "llama-3.1-8b-instant", 
            temperature = 0.1,
            api_key = os.getenv("GROQ_API_KEY")
        )

        logging.info("LLM initialized")

        return llm
    
    except:

        try:

            logging.info("Initializing another LLM")

            llm = ChatGroq(
                model = "llama-3.3-70b-versatile", 
                temperature = 0.1,
                api_key = os.getenv("GROQ_API_KEY")
            )

            logging.info("A different LLM initialized")

            return llm
        
        except Exception as e:

            raise CustomException(e, sys)