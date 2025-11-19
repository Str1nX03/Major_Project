from src.agents.manager_agent import ManagerAgent
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

    def _build_graph(self):

        pass

    def run(self, instructions: dict):

        pass