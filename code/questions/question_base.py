from tkinter import *

class BaseQuestion:
    def __init__(self, question_data: dict) -> None:
        # Question Details
        self.question_id: str = question_data["Question ID"]
        self.question_number: int

        self.question_type: str = question_data["Question Type"]
        self.discarded: bool = question_data["Discarded Question"]

        self.question_text: str = question_data["Question Text"]
        self.question_difficulty: str = question_data["Question Difficulty"]
        self.question_points: int = int(question_data["Question Points"])
        self.fun_fact: str = question_data["Fun Fact"]

        self.question_topics: list[str] = [] # question_data["Question Topics"]
        self.set_topics(question_data["Question Topics"])


        # Question Hints
        self.add_text_hint: bool = question_data["Hints"]["Add Text Hint"]
        self.text_hint: str = question_data["Hints"]["Text Hint"]

        self.text_hint_used: bool = False
        self.relevant_hint_used: bool = False

        self.hint_penalty: float = round(self.question_points / 3, 1)


        # Images
        self.is_image_question: bool = question_data["Images"]["Is Image Question"]
        self.image_file: str = question_data["Images"]["Image File"]


        # Audios
        self.correct_audio: str = question_data["Correct Audio"]
        self.incorrect_audio: str = question_data["Incorrect Audio"]
    
    def set_topics(self, topics: list[str]) -> None:
        for topic in topics: self.question_topics.append(topic)

    def create_dictionary(self) -> dict: return {}

    def included_topics(self, topics: list[str]) -> bool:
        combined: list[str] = self.question_topics + topics
        return len(set(combined)) < len(combined)
    
    def correct_difficulty(self, easy: bool, medium: bool, hard: bool) -> bool:
        match self.question_difficulty:
            case "Easy": return easy
            case "Medium": return medium
            case "Hard": return hard
            case _: return False

    def correct_type(self, closed: bool, open: bool, order: bool) -> bool:
        match self.question_type:
            case "Closed": return closed
            case "Open": return open
            case "Order": return order
            case _: return False