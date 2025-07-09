from questions.answer import Answer
from questions.question_closed import ClosedQuestion

from quiz.answer_past import PastAnswer

class PastClosedQuestion (ClosedQuestion):
    def __init__(self, question_data: dict, extra_details: dict, question_number: int) -> None:
        ClosedQuestion.__init__(self, question_data)

        self.question_number: int = question_number

        self.answers: list[PastAnswer] = self.convert_answers(question_data["Answers"], extra_details)

        self.display_answers()

    def convert_answers(self, answers: list[dict], details: list[dict]) -> list[PastAnswer]:
        return_list: list[PastAnswer] = []

        for i in range(len(answers)):
            return_list.append(PastAnswer([answers[i], details[i]]))
            break

        return return_list
    
    def display_answers(self) -> None:
        for answer in self.answers:
            answer.display_answer()
            print(f"Answer Chosen: {answer.answer_chosen}")
            print(f"Answer Hidden: {answer.answer_hidden}")