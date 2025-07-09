class Answer:
    def __init__(self, answer_data: dict) -> None:
        self.answer_text: str = answer_data["Answer Text"]
        self.answer_back_colour: str = answer_data["Answer Back Colour"]
        self.answer_text_colour: str = answer_data["Answer Text Colour"]

        self.correct_answer: bool = answer_data["Correct Answer"]

        self.answer_number: int = answer_data["Answer Number"]

        self.answer_hidden: bool = False
        self.answer_chosen: bool = False

    def make_dictionary(self) -> dict:
        return {
            "Answer Text": self.answer_text,
            "Answer Back Colour": self.answer_back_colour,
            "Answer Text Colour": self.answer_text_colour,
            "Correct Answer": self.correct_answer,
            "Answer Number": self.answer_number
        }
    
    def make_past_dictionary(self) -> dict:
        return {
            "Answer Text": self.answer_text,
            "Answer Back Colour": self.answer_back_colour,
            "Answer Text Colour": self.answer_text_colour,
            "Correct Answer": self.correct_answer,
            "Answer Number": self.answer_number
        }
    
    def display_answer(self) -> None:
        print(f"Ansewr Number: {self.answer_number}")
        print(f"Answer Text: {self.answer_text}")
        print(f"Answer Colours: {self.answer_back_colour} / {self.answer_text_colour}")
        print(f"Correct Answer: {self.correct_answer}")
