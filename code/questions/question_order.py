from questions.question_base import BaseQuestion

class OrderQuestion(BaseQuestion):
    def __init__(self, question_data: dict) -> None:
        BaseQuestion.__init__(self, question_data)

        # Hints
        self.place_one_hint: bool = question_data["Hints"]["Add Place One Hint"]
        self.placed_word: str = question_data["Hints"]["Provided Word"][0]
        self.placed_index: int = question_data["Hints"]["Provided Word"][1]

        # Answers
        self.correct_order: list[str] = question_data["Answers"]

    def create_dictionary(self) -> dict:
        return {
            "Question ID" : self.question_id,
            "Discarded Question": self.discarded,
            "Question Type" : "Order",
            "Question Text" : self.question_text,
            "Question Difficulty" : self.question_difficulty,
            "Question Points" : self.question_points,
            "Question Topics" : self.question_topics,
            "Hints" : {
                "Add Text Hint" : self.add_text_hint,
                "Text Hint" : self.text_hint,
                "Add Place One Hint" : self.place_one_hint,
                "Provided Word": [self.placed_word, self.placed_index]
            },
            "Images" : {
                "Is Image Question" : self.is_image_question,
                "Image File" : self.image_file
            },
            "Answers" : self.correct_order,
            "Fun Fact": self.fun_fact,
            "Correct Audio" : self.correct_audio,
            "Incorrect Audio" : self.incorrect_audio
        }