from langchain_groq.chat_models import ChatGroq
from src.logger import logging
from src.exception import CustomException
import sys
import os

def get_llm_1():

    if os.getenv("GROQ_API_KEY_1") is None:

        raise Exception("GROQ_API_KEY is not set")

    try:

        logging.info("Initializing LLM")

        llm = ChatGroq(
            model = "llama-3.1-8b-instant", 
            temperature = 0.1,
            api_key = os.getenv("GROQ_API_KEY_1")
        )

        logging.info("LLM initialized")

        return llm
    
    except Exception as e:

        raise CustomException(e, sys)
        
def get_llm_lite_1():

    if os.getenv("GROQ_API_KEY_1") is None:

        raise Exception("GROQ_API_KEY is not set")

    try:

        logging.info("Initializing LLM")

        llm = ChatGroq(
            model = "llama-3.3-70b-versatile", 
            temperature = 0.1,
            api_key = os.getenv("GROQ_API_KEY_1")
        )

        logging.info("LLM initialized")

        return llm
    
    except Exception as e:

        raise CustomException(e, sys)
    
def get_llm_2():

    if os.getenv("GROQ_API_KEY_2") is None:

        raise Exception("GROQ_API_KEY is not set")

    try:

        logging.info("Initializing LLM")

        llm = ChatGroq(
            model = "llama-3.1-8b-instant", 
            temperature = 0.1,
            api_key = os.getenv("GROQ_API_KEY_2")
        )

        logging.info("LLM initialized")

        return llm
    
    except Exception as e:

        raise CustomException(e, sys)
        
def get_llm_lite_2():

    if os.getenv("GROQ_API_KEY_2") is None:

        raise Exception("GROQ_API_KEY is not set")

    try:

        logging.info("Initializing LLM")

        llm = ChatGroq(
            model = "llama-3.3-70b-versatile", 
            temperature = 0.1,
            api_key = os.getenv("GROQ_API_KEY_2")
        )

        logging.info("LLM initialized")

        return llm
    
    except Exception as e:

        raise CustomException(e, sys)
