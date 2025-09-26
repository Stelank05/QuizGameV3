from questions.answer import Answer
from questions.question_base import BaseQuestion

class ClosedQuestion(BaseQuestion):
    def __init__(self, question_data: dict) -> None:
        BaseQuestion.__init__(self, question_data)

        # Hints
        self.add_50_50_hint: bool = question_data["Hints"]["Add 50/50 Hint"]

        # Answers
        self.answers: list[Answer] = ClosedQuestion.create_answers(question_data["Answers"])

    def create_answers(answers: list[dict]) -> list[Answer]:
        return_list: list[Answer] = []

        for answer in answers:
            return_list.append(Answer(answer))

        return return_list

    def create_dictionary(self) -> dict:
        return {
            "Question ID" : self.question_id,
            "Discarded Question": self.discarded,
            "Question Type" : self.question_type,
            "Question Text" : self.question_text,
            "Question Difficulty" : self.question_difficulty,
            "Question Points" : self.question_points,
            "Question Topics" : self.question_topics,
            "Hints" : {
                "Add Text Hint" : self.add_text_hint,
                "Text Hint" : self.text_hint,
                "Add 50/50 Hint" : self.add_50_50_hint
            },
            "Images" : {
                "Is Image Question" : self.is_image_question,
                "Image File" : self.image_file
            },
            "Answers" : self.make_answer_dicts(),
            "Fun Fact": self.fun_fact,
            "Correct Audio" : self.correct_audio,
            "Incorrect Audio" : self.incorrect_audio
        }
    
    def make_answer_dicts(self) -> list[dict]:
        return_list: list[dict] = []

        for answer in self.answers:
            return_list.append(answer.make_dictionary())

        return return_list