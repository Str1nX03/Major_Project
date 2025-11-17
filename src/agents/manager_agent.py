from src.utils import get_llm
from src.logger import logging
from src.exception import CustomException
from langgraph.graph import StateGraph, END, START
import sys
from typing import TypedDict

class AgentState(TypedDict):

    standard: str
    subject: str
    instructions: str
    topic: str

class ManagerAgent:

    def __init__(self):

        self.llm = get_llm()
        self.graph = self._build_graph()

    def _build_graph(self):

        graph = StateGraph(AgentState)

        # Graph Logic and Structure will go here

        return graph.compile()

    def run(self, topic: str, subject: str, standard: int):

        try:

            logging.info("Running Manager Agent...")

            initial_state = {"standard": standard, "subject": subject, "topic": topic}
            final_state = self.graph.invoke(input = initial_state)

            logging.info("Manager Agent's work Finished and instructions are ready to be sent to other agents...")

            return final_state["instructions"]

        except Exception as e:

            raise CustomException(e, sys)