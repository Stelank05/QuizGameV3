from questions.question_open import OpenQuestion

class PastOpenQuestion (OpenQuestion):
    def __init__(self, question_data: dict, extra_details: list[dict] | None, question_number: int) -> None:
        OpenQuestion.__init__(self, question_data)

        self.question_number = question_number

        self.awarded_points: float = 0.0

        self.entered_answer: str = ""

        if extra_details != None:
            self.answered_correctly = extra_details["Answered Correctly"]
            self.awarded_points = extra_details["Awarded Points"]
            self.text_hint_used = extra_details["Text Hint Used"]
            self.relevant_hint_used = extra_details["Open Hint Used"]
            self.entered_answer = extra_details["Entered Answer"]

    def create_past_dict(self) -> dict:
        return {
            "Question ID": self.question_id,
            "Question Type": self.question_type,
            "Extra Details": {
                "Question Number": self.question_number,
                "Answered Correctly": self.answered_correctly,
                "Awarded Points": self.awarded_points,
                "Text Hint Used": self.text_hint_used,
                "Open Hint Used": self.relevant_hint_used,
                "Entered Answer": self.entered_answer
            }
        }
    
    def valid_answer(self, user_answer: str) -> bool:
        self.entered_answer = user_answer
        return OpenQuestion.valid_answer(self, user_answer)