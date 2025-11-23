from src.utils import get_llm_1, get_llm_lite_1
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

class AssistantAgent:

    def __init__(self):

        self.llm_lite = get_llm_lite_1()
        self.llm = get_llm_1()
        self.graph = self._build_graph()
        self.tool = [TavilySearch(
            max_results = 5,
            topic = "general",
            api_key = os.getenv("TAVILY_API_KEY")
        )]

    def _build_graph(self):

        graph = StateGraph(AgentState)

        # Graph Logic and Structure will go here
        graph.add_node("generate_instructions", self._generate_instructions)
        graph.add_node("user_interaction", self._user_interaction)
        graph.add_node("generate_study_links", self._generate_study_links)

        graph.add_edge(START, "generate_study_links")
        graph.add_edge("generate_study_links", "user_interaction")
        graph.add_edge("user_interaction", "generate_instructions")
        graph.add_edge("generate_instructions", END)
        return graph.compile()
    
    def _user_interaction(self, state: AgentState) -> dict:

        try:

            logging.info("Agent is generating initial contents for the user...")

            topic = state["topic"]
            subject = state["subject"]
            standard = state["standard"]
            study_links = state["study_links"]

            prompt = f"""

            You are a manager and a teacher. Your task is to provide the instructions to the user for a particular topic.
            You will give a general idea about the topic like how difficult it is and what are the pre-requisites to study the topic.
            You will also give a brief introduction on this topic to the user.
            
            These are the general instructions provided by the user:-

            1. The topic that is needed to be taught to the user is :- {topic}
            2. The subject that is needed to be taught to the user is :- {subject}
            3. The standard that the user currently is in with respect to Indian standard (School) :- {standard}

            These are the study materials and general intro provided by the user:-

            {study_links}

            So provide the links of the study materials and intro to the study materials as well along with the general intro to the topic.
            Also add tips for learning the topic.

            IMPORTANT FORMATTING INSTRUCTIONS:
            - The output MUST be in HTML format.
            - Use <h3> tags for main headings.
            - Use <b> tags for bold text (do not use asterisks **).
            - Use <p> tags for paragraphs.
            - Use <ul> and <li> tags for lists.
            - Ensure the content is visually structured and easy to read.
            - Do NOT use Markdown syntax (like #, *, -).

            """

            response = self.llm_lite.invoke([SystemMessage(content=prompt)])

            logging.info("Agent has generated initial contents for the user...")

            return {"topic_intro": response.content}

        except Exception as e:

            raise CustomException(e, sys)

    def _generate_instructions(self, state: AgentState) -> dict:

        try:
            
            logging.info("Agent is generating instructions for the agents...")

            standard = state["standard"]
            subject = state["subject"]
            topic_intro = state["topic_intro"]
            study_links = state["study_links"]
            topic = state["topic"]

            prompt = f"""

            You are an agent manager and your task is to write a detailed prompt for an agent whose task is to plan lessons based on:-

            1. The topic that is needed to be taught to the user is :- {topic}
            2. The subject that is needed to be taught to the user is :- {subject}
            3. The standard that the user currently is in with respect to Indian standard (School) :- {standard}
            4. The study materials and general intro provided for the user:- {study_links}
            5. The general intro provided for the user: {topic_intro}
            
            Give explicit prompt for the planning agent only, the agent should plan the lessons step by step and in comprehensive way so that even user will get time to be comfortable with the topics.
            Your instructions should be in separate sections like this:-
            
            1. This section will contain the topic intro: {topic_intro}
            2. This section will contain general info about the user's requests i.e. topic: {topic}, subject: {subject}, standard: {standard}
            3. This section must include the study links url ({study_links}) for the planning agent.
            4. This section will contain the pre requisites and difficulty level for the topic.
            5. This section will contain explicit prompt for the planning agent, the agent should plan the lessons step by step and in comprehensive way (35 - 50 lessons) so that even user will get time to be comfortable with the topics.

            You must only give the prompt for the planning agent and you do not have to plan the lessons.

            """

            response = self.llm.invoke(prompt)

            logging.info("Agent has generated instructions for the agents...")

            return {"instructions": response.content}

        except Exception as e:

            raise CustomException(e, sys)

    def _generate_study_links(self, state: AgentState) -> str:

        try:

            logging.info("Agent is generating study materials and general intro for the user...")

            topic = state["topic"]
            subject = state["subject"]
            standard = state["standard"]

            prompt = f"""

            Give me a study materials, youtube video links and general intro on the topic: {topic} from the subject: {subject} for the student of standard: {standard}.

            """

            response = self.tool[0].invoke(prompt)

            # Defensive check: Ensure response is a string
            if not isinstance(response, str):
                if isinstance(response, list):
                    items = []
                    for item in response:
                        if isinstance(item, dict):
                            items.append(f"{item.get('url', str(item))}")
                        else:
                            items.append(str(item))
                    response = "\n".join(items)
                else:
                    response = str(response)

            logging.info("Agent has generated study materials and general intro for the user...")

            return {"study_links": response}
        
        except Exception as e:

            raise CustomException(e, sys)

    def run(self, topic: str, subject: str, standard: int):

        try:

            logging.info("Running Manager Agent...")

            initial_state = {"standard": standard, "subject": subject, "topic": topic}
            final_state = self.graph.invoke(input = initial_state)

            logging.info("Manager Agent's work Finished...")

            return final_state["instructions"]
        
        except Exception as e:

            raise CustomException(e, sys)