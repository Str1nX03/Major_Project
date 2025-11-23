from src.utils import get_llm_2, get_llm_lite_2
from src.logger import logging
from src.exception import CustomException
from langgraph.graph import StateGraph, END, START
from typing import TypedDict
import sys

class AgentState(TypedDict):

    lessons: dict
    tests: dict

class TestingAgent:

    def __init__(self):

        self.llm = get_llm_2()
        self.llm_lite = get_llm_lite_2()
        self.graph = self._build_graph()

    def _build_graph(self):

        graph = StateGraph(AgentState)

        # Graph Logic and Structure will go here
        graph.add_node("generate_tests", self._generate_tests)

        graph.add_edge(START, "generate_tests")
        graph.add_edge("generate_tests", END)

        return graph.compile()

    def _generate_tests(self, state: AgentState) -> dict:

        try:

            logging.info("Testing Agent is generating tests with solutions...")

            lessons = state["lessons"]
            tests = {}
            lesson_list = list(lessons.keys())
            lessons_length = len(lesson_list)

            # Common instructions for HTML formatting
            formatting_instructions = """
            IMPORTANT FORMATTING INSTRUCTIONS:
            - Provide the output in strictly HTML format.
            - Use <b> for questions and headers (e.g., <b>Question 1:</b>).
            - Use <p> for the question body and solution text.
            - Use <br> for line breaks where necessary.
            - Do NOT use asterisks (*) or markdown.
            - Make the solution and revision notes distinct using <p> tags.
            """

            for lesson in lesson_list[:lessons_length//2]:

                prompt = f"This is the lesson intro: {lesson}. Generate 1 test question as user's question paper along with its solutions based on those lessons in such a way that the lesson can be revised by the user after the test. {formatting_instructions}"
                test = self.llm_lite.invoke(prompt)
                tests[lesson] = test.content

            for lesson in lesson_list[lessons_length//2:]:

                prompt = f"This is the lesson intro: {lesson}. Generate 1 test question as user's question paper along with its solutions based on those lessons in such a way that the lesson can be revised by the user after the test. {formatting_instructions}"
                test = self.llm.invoke(prompt)
                tests[lesson] = test.content

            logging.info("Testing Agent has generated tests with solutions...")

            return {"tests": tests}

        except Exception as e:

            raise CustomException(e, sys)

    def run(self, lessons: dict):

        try:

            logging.info("Running Testing Agent...")

            initial_state = {"lessons": lessons}
            final_state = self.graph.invoke(input = initial_state)

            logging.info("Testing Agent's work Finished...")

            return final_state["tests"]

        except Exception as e:

            raise CustomException(e, sys)