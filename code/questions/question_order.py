from questions.question_base import BaseQuestion

class OrderQuestion(BaseQuestion):
    def __init__(self, question_data: dict) -> None:
        BaseQuestion.__init__(self, question_data)

        # Hints
        self.place_one_hint: bool = question_data["Hints"]["Add Place One Hint"]
        self.placed_item: tuple = question_data["Hints"]["Placed Item"]

        # Answers
        self.correct_order: list[str] = question_data["Answers"]["Correct Order"]
        self.display_order: str | list[str] = question_data["Answers"]["Display Order"]

    def create_dictionary(self) -> dict: return {}