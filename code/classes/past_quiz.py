from questions.answer import Answer
from questions.question_base import BaseQuestion

class PastQuiz:
    def __init__(self, past_quiz_data: dict) -> None:
        self.quiz_id: str = past_quiz_data["Quiz ID"]
        self.score: float = past_quiz_data["Score"]
        self.percentage: float = past_quiz_data["Percentage"]
        self.questions: list[BaseQuestion] = self.load_questions(past_quiz_data["Questions"])

    def load_questions(self, questions: list[str]) -> list[BaseQuestion]:
        return []
    
    def make_dictionary(self) -> dict:
        return {}