import random

from questions.question_closed import ClosedQuestion

from quiz.answer_past import PastAnswer

class PastClosedQuestion (ClosedQuestion):
    def __init__(self, question_data: dict, extra_details: list[dict] | None, question_number: int) -> None:
        ClosedQuestion.__init__(self, question_data)

        self.question_number: int = question_number

        self.awarded_points: float = 0.0
        if extra_details != None: self.awarded_points = extra_details["Awarded Points"]
        
        self.answers: list[PastAnswer] = []
        if extra_details != None: self.answers = self.convert_answers(question_data["Answers"], extra_details["Answers"])
        else: self.answers = self.convert_answers(question_data["Answers"], None)

        self.randomise_display_order()
        # self.display_answers()

    def convert_answers(self, answers: list[dict], details: list[dict] | None) -> list[PastAnswer]:
        return_list: list[PastAnswer] = []

        for i in range(len(answers)):
            if details == None: return_list.append(PastAnswer([answers[i], details]))
            else: return_list.append(PastAnswer([answers[i], details[i]]))
            # break

        return return_list
    
    def randomise_display_order(self) -> None:
        order_numbers: list[int] = list(range(len(self.answers)))

        number: int
        for answer in self.answers:
            number = random.choice(order_numbers)
            order_numbers.remove(number)
            answer.display_index = number
    
    def display_answers(self) -> None:
        for answer in self.answers:
            answer.display_answer()
            print(f"Display Index: {answer.display_index}")
            print(f"Answer Chosen: {answer.answer_chosen}")
            print(f"Answer Hidden: {answer.answer_hidden}")
            print()
    
    def create_past_dict(self) -> dict:
        return {
            "Question ID": self.question_id,
            "Question Type": self.question_type,
            "Extra Details": {
                "Awarded Points": self.awarded_points,
                "Answers": self.make_answer_details()
            }
        }
    
    def make_answer_details(self) -> list[dict]:
        return_list: list[dict] = []

        for answer in self.answers:
            return_list.append({
                "Display Index": answer.display_index,
                "Answer Chosen": answer.answer_chosen,
                "Answer Hidden": answer.answer_hidden
            })

        return return_list