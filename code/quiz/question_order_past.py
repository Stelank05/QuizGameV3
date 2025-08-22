import random

from tkinter import *

from questions.question_order import OrderQuestion

class PastOrderQuestion (OrderQuestion):
    def __init__(self, question_data: dict, extra_details: list[dict] | None, question_number: int) -> None:
        OrderQuestion.__init__(self, question_data)

        self.question_number = question_number

        self.awarded_points: float = 0.0

        self.displayed_order: list[str] = []
        self.entered_order: list[tuple[int, str]] = []

        if extra_details != None:
            self.answered_correctly = extra_details["Answered Correctly"]
            self.awarded_points = extra_details["Awarded Points"]
            self.text_hint_used = extra_details["Text Hint Used"]
            self.relevant_hint_used = extra_details["Order Hint Used"]
            self.displayed_order = extra_details["Displayed Answer Order"]
            self.entered_order = extra_details["Entered Answer Order"]
        else:
            self.displayed_order = self.randomise_display_order()
    
    def randomise_display_order(self) -> list[str]:
        return_list: list[str] = []
        correct_order: list[str] = self.correct_order.copy()

        chosen_item: str

        while len(correct_order) > 0:
            chosen_item = random.choice(correct_order)
            correct_order.remove(chosen_item)
            return_list.append(chosen_item)

        return return_list

    def create_past_dict(self) -> dict:
        return {
            "Question ID": self.question_id,
            "Question Type": self.question_type,
            "Extra Details": {
                "Question Number": self.question_number,
                "Answered Correctly": self.answered_correctly,
                "Awarded Points": self.awarded_points,
                "Text Hint Used": self.text_hint_used,
                "Order Hint Used": self.relevant_hint_used,
                "Displayed Answer Order": self.displayed_order,
                "Entered Answer Order": self.entered_order
            }
        }
    
    def valid_answer(self, user_answer: list[tuple[int, str]]) -> bool:
        user_answer = PastOrderQuestion.order_input(user_answer)
        
        for i in range(len(user_answer)):
            if user_answer[i][1] != self.correct_order[i]: return False

        return True
        
    def order_input(user_answer: list[tuple[int, str]]) -> list[tuple[int, str]]:
        swap: bool
        temp: tuple[int, str]

        for i in range(len(user_answer) - 1):
            swap = False

            for j in range(len(user_answer) - i - 1):
                if user_answer[j][0] > user_answer[j + 1][0]:
                    swap = True

                    temp = user_answer[j]
                    user_answer[j] = user_answer[j + 1]
                    user_answer[j + 1] = temp

            if not swap: break
        
        return user_answer