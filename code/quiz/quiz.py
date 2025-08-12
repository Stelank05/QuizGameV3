import random

from controls.sort_functions import *

from questions.answer import Answer
from questions.question_base import BaseQuestion

from quiz.question_closed_past import PastClosedQuestion
from quiz.question_open_past import PastOpenQuestion
from quiz.question_order_past import PastOrderQuestion

from window.window_components import WindowComponents

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
        self.hints_used: int = 0

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
            "Hints Used": self.hints_used,
            "Questions": self.create_question_list()
        }
    
    def generate_quiz_id(self) -> str:
        if len(CommonData.past_quizzes) == 0: return "PQ0001"
        id_sort_quizzes(CommonData.past_quizzes)
        return f"PQ{str(int(CommonData.past_quizzes[-1].quiz_id.replace("PQ", "")) + 1).rjust(4, "0")}"
    
    def create_question_list(self) -> list[dict]:
        return_list: list[dict] = []

        for question in self.questions:
            return_list.append(question.create_past_dict())

        return return_list

    def select_questions(self) -> None:
        question_list: list[tuple[str, int]] = []

        numbers: list[int] = list(range(len(WindowComponents.available_question_codes)))
        number: int

        for question in WindowComponents.available_question_codes:
            number = random.choice(numbers)
            question_list.append((question, number))
            numbers.remove(number)

        temp: tuple[str, int]
        swap: bool

        for i in range(len(question_list) - 1):
            swap = False
            for j in range(len(question_list) - i - 1):
                if question_list[j][1] > question_list[j + 1][1]:
                    swap = True
                    temp = question_list[j]
                    question_list[j] = question_list[j + 1]
                    question_list[j + 1] = temp

            if not swap: break

        question: BaseQuestion

        for question_number in range(int(WindowComponents.quiz_length.get())): #len(question_list)):
            question = CommonData.get_question(question_list[question_number][0], CommonData.usable_questions, 0, len(CommonData.usable_questions))
        
            match question.question_type:
                case "Closed": self.questions.append(PastClosedQuestion(question.create_dictionary(), None, question_number + 1))
                case "Open": self.questions.append(PastOpenQuestion(question.create_dictionary(), None, question_number + 1))
                case "Order": self.questions.append(PastOrderQuestion(question.create_dictionary(), None, question_number + 1))
        