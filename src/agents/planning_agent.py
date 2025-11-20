from src.utils import get_llm
from src.logger import logging
from src.exception import CustomException
from langgraph.graph import StateGraph, END, START
from langchain_tavily import TavilySearch
from typing import TypedDict
import sys
import os

class AgentState(TypedDict):

    instructions: str
    study_links: list
    lessons: dict

class PlannerAgent:

    def __init__(self):

        self.llm = get_llm()
        self.graph = self._build_graph()
        self.tool = [TavilySearch(
            max_results = 3,
            topic = "general",
            api_key = os.getenv("TAVILY_API_KEY")
        )]
        
    def _get_links_info(self, state: AgentState) -> dict:

        pass

    def _build_graph(self):

        pass

    def run(self, instructions: str, study_links: list):

        try: 
            
            logging.info("Running Planning Agent...")

            initial_state = {"instructions": instructions, "study_links": study_links}
            final_state = self.graph.invoke(input = initial_state)

            logging.info("Planning Agent's work Finished...")

            return "I got the instructions"

        except Exception as e:

            raise CustomException(e, sys)