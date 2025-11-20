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

        pass

    def run(self, lessons: dict):

        pass