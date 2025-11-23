from src.utils import get_llm_1, get_llm_lite_1
from src.logger import logging
from src.exception import CustomException
from langgraph.graph import StateGraph, END, START
from typing import TypedDict
import sys

class AgentState(TypedDict):

    instructions: str
    standard: int
    subject: str
    topic: str
    lessons: dict
    plannings: str

class TutoringAgent:

    def __init__(self):

        self.llm_lite = get_llm_lite_1()
        self.llm = get_llm_1()
        self.graph = self._build_graph()

    def _build_graph(self):

        graph = StateGraph(AgentState)
        
        # Graph Logic and Structure will go here
        graph.add_node("get_lesson_plannings", self._get_lesson_plannings)
        graph.add_node("get_lessons", self._get_lessons)

        graph.add_edge(START, "get_lesson_plannings")
        graph.add_edge("get_lesson_plannings", "get_lessons")
        graph.add_edge("get_lessons", END)
        
        return graph.compile()
    
    def _get_lesson_plannings(self, state: AgentState) -> dict:

        try:

            logging.info("Planning Agent is generating lesson's planning...")

            instructions = state["instructions"]
            standard = state["standard"]
            subject = state["subject"]
            topic = state["topic"]

            prompt = f"""

            You must read the instructions: {instructions} and plan the lessons step by step for the topic: {topic}, subject: {subject}, for the students of standard: {standard} and in comprehensive way so that even user will get time to be comfortable with the topics.
            Make the length of the lessons for about 35-50 lessons depending on the topic and its difficulty level.
            You must only generate the lessons and mark numbers to the lessons chronologically and in a step by step manner.
            Dont write literally anything else, just write the lesson number, lesson title, all the topics we will learn in that specific lesson and thats it.
            Just list down lessons in only this manner, no need to write anything else.

            """

            response = self.llm_lite.invoke(prompt)

            logging.info("Planning Agent has generated lesson's planning...")

            return {"plannings": response.content}

        except Exception as e:

            raise CustomException(e, sys)
        
    def _get_lessons(self, state: AgentState) -> dict:

        try:

            logging.info("Planning Agent is generating lessons...")

            plannings = state["plannings"]
            topic = state["topic"]
            lessons = {}
            lesson_list = plannings.split("\n")

            for lesson in lesson_list:
    
                prompt = f"""
                
                You must generate comprehensive and detailed lesson contents for the lesson: {lesson}
                Make it in such a way that nothing else will be needed for the topic.
                Also if the topic: {topic} is related to or closely depends upon mathematics, then make the lessons more mathematical and less theory based.

                IMPORTANT FORMATTING INSTRUCTIONS:
                - The output MUST be in HTML format.
                - Use <h4> for section headers.
                - Use <b> for bold text (do NOT use asterisks like **text**).
                - Use <p> for paragraphs.
                - Use <ul> and <li> for lists.
                - Do NOT use Markdown.
                
                """
                response = self.llm.invoke(prompt)
                lessons[lesson] = response.content     

            logging.info("Planning Agent has generated lessons...")

            return {"lessons": lessons}

        except Exception as e:

            raise CustomException(e, sys)

    def run(self, instructions: str, standard: int, subject: str, topic: str):

        try: 
            
            logging.info("Running Planning Agent...")

            initial_state = {"instructions": instructions, "standard": standard, "subject": subject, "topic": topic}
            final_state = self.graph.invoke(input = initial_state)

            logging.info("Planning Agent's work Finished...")

            return final_state["lessons"]

        except Exception as e:

            raise CustomException(e, sys)