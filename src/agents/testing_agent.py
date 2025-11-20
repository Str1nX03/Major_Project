from src.utils import get_llm
from src.logger import logging
from src.exception import CustomException
from langgraph.graph import StateGraph, END, START
from langchain_tavily import TavilySearch
from typing import TypedDict
import sys
import os


class AgentState(TypedDict):
    
    lessons: dict
    tests: dict

class TestingAgent:

    def __init__(self):

        self.llm = get_llm()
        self.graph = self._build_graph()

    def _build_graph(self):

        graph = StateGraph(AgentState)

        # Graph Logic and Structure will go here
        
        return graph.compile()

    def run(self, lessons: dict):

        try:

            logging.info("Running Testing Agent...")

            initial_state = {"lessons": lessons}
            final_state = self.graph.invoke(input = initial_state)

            logging.info("Testing Agent's work Finished...")

            return final_state["tests"]

        except Exception as e:

            raise CustomException(e, sys)