import random

from controls.sort_functions import *

from questions.answer import Answer
from questions.question_base import BaseQuestion

from quiz.question_closed_past import PastClosedQuestion
from quiz.question_open_past import PastOpenQuestion
from quiz.question_order_past import PastOrderQuestion

# from window.window_components import WindowComponents

from common_data import CommonData

class Quiz:
    def __init__(self) -> None:
        self.quiz_id: str

        self.questions: list[BaseQuestion] = []

        self.question_number: int = 1

        self.current_score: float = 0.0
        self.theoretical_max: float = 0.0
        self.score_percentage: float = 0.0

        self.correct_count: int = 0
        self.incorrect_count: int = 0
        
        self.text_hints_used: int = 0
        self.closed_hints_used: int = 0
        self.open_hints_used: int = 0
        self.order_hints_used: int = 0

        self.quiz_complete: bool = False

    def create_dictionary(self, player_id: str) -> dict:
        return {
            "Quiz ID": self.generate_quiz_id(),
            "Player ID": player_id,
            "Score": self.current_score,
            "Max Score": self.theoretical_max,
            "Percentage": self.score_percentage,
            "Correct Count": self.correct_count,
            "Incorrect Count": self.incorrect_count,
            "Total Hints Used": self.text_hints_used + self.closed_hints_used + self.open_hints_used + self.order_hints_used,
            "Text Hints Used": self.text_hints_used,
            "Closed Hints Used": self.closed_hints_used,
            "Open Hints Used": self.open_hints_used,
            "Order Hints Used": self.order_hints_used,
            "Questions": self.create_question_list()
        }
    
    def generate_quiz_id(self) -> str:
        if len(CommonData.past_quizzes) == 0: return "PQ0001"
        sort_quizzes_id(CommonData.past_quizzes)
        return f"PQ{str(int(CommonData.past_quizzes[-1].quiz_id.replace("PQ", "")) + 1).rjust(4, "0")}"
    
    def create_question_list(self) -> list[dict]:
        return_list: list[dict] = []

        for question in self.questions:
            return_list.append(question.create_past_dict())

        return return_list

    def select_questions(self, question_codes: list[str], quiz_length: int) -> None:
        question_list: list[str] = []

        # question_codes: list[str] = WindowComponents.available_question_codes.copy()
        question_code: str

        while len(question_list) < int(quiz_length):
            question_code = random.choice(question_codes)
            question_codes.remove(question_code)
            question_list.append(question_code)

        question: BaseQuestion

        for question_number in range(len(question_list)):
            question = CommonData.get_question(question_list[question_number], CommonData.usable_questions, 0, len(CommonData.usable_questions))
            
            match question.question_type:
                case "Closed": self.questions.append(PastClosedQuestion(question.create_dictionary(), None, question_number + 1))
                case "Open": self.questions.append(PastOpenQuestion(question.create_dictionary(), None, question_number + 1))
                case "Order": self.questions.append(PastOrderQuestion(question.create_dictionary(), None, question_number + 1))
        
    def randomise_questions(self, questions: list[BaseQuestion]) -> None:
        question: BaseQuestion

        while len(questions) > 0:
            question = random.choice(questions)
            questions.remove(question)
            self.questions.append(question)