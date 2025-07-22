from questions.question_base import BaseQuestion

class OpenQuestion(BaseQuestion):
    def __init__(self, question_data: dict) -> None:
        BaseQuestion.__init__(self, question_data)

        # Hints
        self.provide_word_hint: bool = question_data["Hints"]["Add Provide Word Hint"]
        self.provided_word: str = question_data["Hints"]["Provided Word"]

        # Answers
        self.required_words: list[str] = question_data["Answers"]["Required Words"]
        self.acceptable_words: list[str] = question_data["Answers"]["Acceptable Words"]
    
    def valid_answer(self, user_answer: str) -> bool:
        user_answer = user_answer.lower()

        for word in user_answer:
            print(word)
            print(word in self.required_words) ; print(word in self.acceptable_words)
            if word not in self.required_words and word not in self.acceptable_words:
                return False
            
        return True

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
                "Add Provide Word Hint" : self.provide_word_hint,
                "Provided Word": self.provided_word
            },
            "Images" : {
                "Is Image Question" : self.is_image_question,
                "Image File" : self.image_file
            },
            "Answers" : {
                "Required Words" : self.required_words,
                "Acceptable Words" : self.acceptable_words
            },
            "Fun Fact": self.fun_fact,
            "Correct Audio" : self.correct_audio,
            "Incorrect Audio" : self.incorrect_audio
        }