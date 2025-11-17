from src.utils import get_llm
from src.logger import logging
from src.exception import CustomException
from langgraph.graph import StateGraph, END, START
from langchain_tavily import TavilySearch
from langchain_core.messages import SystemMessage
import sys
import os
from typing import TypedDict

class AgentState(TypedDict):

    standard: str
    subject: str
    instructions: str
    topic_intro: str
    study_links: str
    topic: str

class ManagerAgent:

    def __init__(self):

        self.llm = get_llm()
        self.graph = self._build_graph()
        self.tool = [TavilySearch(
            max_results = 3,
            topic = "general",
            api_key = os.getenv("TAVILY_API_KEY")
        )]

    def _build_graph(self):

        graph = StateGraph(AgentState)

        # Graph Logic and Structure will go here
        graph.add_node("generate_instructions", self._generate_instructions)
        graph.add_node("user_interaction", self._user_interaction)
        graph.add_node("generate_study_links", self._generate_study_links)

        return graph.compile()
    
    def _user_interaction(self, state: AgentState) -> dict:

        topic = state["topic"]
        subject = state["subject"]
        standard = state["standard"]
        study_links = state["study_links"]

        prompt = f"""

        You are a teacher. Your task is to provide the instructions to the user for a particular topic.
        You will give a general idea about the topic like how difficult it is and what are the pre-requisites to study the topic.
        You will also give a brief introduction on this topic to the user.
        
        These are the general instructions provided by the user:-

        1. The topic that is needed to be taught to the user is :- {topic}
        2. The subject that is needed to be taught to the user is :- {subject}
        3. The standard that the user currently is in with respect to Indian standard (School) :- {standard}

        These are the study materials and general intro provided by the user:-

        {study_links}

        So provide the links of the study materials and intro to the study materials as well along with the general intro to the topic.

        """

        response = self.llm.invoke([SystemMessage(content=prompt)])

        return {"topic_intro": response.content}

    def _generate_instructions(self, state: AgentState) -> str:

        pass

    def _generate_study_links(self, state: AgentState) -> str:

        topic = state["topic"]
        subject = state["subject"]
        standard = state["standard"]

        prompt = f"""

        Give me a study materials and general intro on the topic: {topic} from the subject: {subject} for the student of standard: {standard}.

        """

        response = self.tool[0].invoke([SystemMessage(content=prompt)])

        return {"study_links": response}

    def run(self, topic: str, subject: str, standard: int):

        try:

            logging.info("Running Manager Agent...")

            initial_state = {"standard": standard, "subject": subject, "topic": topic}
            final_state = self.graph.invoke(input = initial_state)

            logging.info("Manager Agent's work Finished and instructions are ready to be sent to other agents...")

            return final_state["instructions"]

        except Exception as e:

            raise CustomException(e, sys)