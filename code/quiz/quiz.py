import random

# from copy import copy, deepcopy

from questions.answer import Answer
from questions.question_base import BaseQuestion

from quiz.question_closed_past import PastClosedQuestion
from quiz.question_open_past import PastOpenQuestion

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

        self.quiz_complete: bool = False

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
            # print(f"{question.question_id}") # - {question.question_difficulty} / {question.question_type} / {question.is_image_question}")

            match question.question_type:
                case "Closed": self.questions.append(PastClosedQuestion(question.create_dictionary(), None, question_number + 1))
                case "Open": self.questions.append(PastOpenQuestion(question.create_dictionary(), None, question_number + 1))
                case "Order": print()
        
        # print()


        # self.questions = question_list