from questions.question_open import OpenQuestion

class PastOpenQuestion (OpenQuestion):
    def __init__(self, question_data: dict, extra_details: list[dict] | None, question_number: int) -> None:
        OpenQuestion.__init__(self, question_data)

        self.question_number = question_number

        self.entered_answer: str = ""

        self.awarded_points: float = 0.0

        if extra_details != None:
            self.awarded_points = extra_details["Awarded Points"]
            self.entered_answer = extra_details["Entered Answer"]

    def create_past_dict(self) -> dict:
        return {
            "Question ID": self.question_id,
            "Question Type": self.question_type,
            "Extra Details": {
                "Awarded Points": self.awarded_points,
                "Entered Answer": self.entered_answer
            }
        }