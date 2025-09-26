import os

from controls.file_handler import *

from questions.question_base import BaseQuestion

from quiz.question_closed_past import PastClosedQuestion
from quiz.question_open_past import PastOpenQuestion
from quiz.question_order_past import PastOrderQuestion

class PastQuiz:
    def __init__(self, past_quiz_data: dict, question_list: list[BaseQuestion] = None, question_folder: str = None) -> None:
        self.quiz_id: str = past_quiz_data["Quiz ID"]

        self.player_id: str = past_quiz_data["Player ID"]

        self.score: float = past_quiz_data["Score"]
        self.max_score: float = past_quiz_data["Max Score"]
        self.percentage: float = past_quiz_data["Percentage"]

        self.correct_count: int = past_quiz_data["Correct Count"]
        self.incorrect_count: int = past_quiz_data["Incorrect Count"]

        self.total_hints_used: int = past_quiz_data["Total Hints Used"]
        self.text_hints_used: int = past_quiz_data["Text Hints Used"]
        self.closed_hints_used: int = past_quiz_data["Closed Hints Used"]
        self.open_hints_used: int = past_quiz_data["Open Hints Used"]
        self.order_hints_used: int = past_quiz_data["Order Hints Used"]

        if question_list == None: self.questions = self.load_past_questions(past_quiz_data["Questions"], question_folder)
        else: self.questions = question_list
        
        self.correct_percentage: int = round((self.correct_count / len(self.questions)) * 100, 1)
 
    def __str__(self) -> str:
        return f"{self.quiz_id} - {len(self.questions)} Questions"

    def create_dictionary(self) -> dict:
        return {
            "Quiz ID": self.quiz_id,
            "Score": self.score,
            "Max Score": self.max_score,
            "Percentage": self.percentage,
            "Correct Count": self.correct_count,
            "Incorrect count": self.incorrect_count,
            "Hints Used": self.hints_used,
            "Questions": self.create_question_list()
        }
    
    def create_question_list(self) -> list[dict]:
        return_list: list[dict] = []

        for question in self.questions:
            return_list.append(question.create_past_dict())

        return return_list

    def load_past_questions(self, questions: list[dict], question_folder) -> list[BaseQuestion]:
        return_list: list[BaseQuestion] = []

        question_dict: dict
        for question in questions:
            match question["Question Type"]:
                case "Closed":
                    question_dict = read_json_file(os.path.join(question_folder, f"{question["Question ID"]}.json"))
                    return_list.append(PastClosedQuestion(question_dict, question["Extra Details"], question["Extra Details"]["Question Number"]))
                case "Open":
                    question_dict = read_json_file(os.path.join(question_folder, f"{question["Question ID"]}.json"))
                    return_list.append(PastOpenQuestion(question_dict, question["Extra Details"], question["Extra Details"]["Question Number"]))
                case "Order":
                    question_dict = read_json_file(os.path.join(question_folder, f"{question["Question ID"]}.json"))
                    return_list.append(PastOrderQuestion(question_dict, question["Extra Details"], question["Extra Details"]["Question Number"]))

        return return_list