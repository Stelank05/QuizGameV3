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
    
    def valid_answer(self, input_answer: str) -> bool:
        user_answer: list[str] = input_answer.lower().split(' ')
        
        # print(user_answer)
        # print(self.required_words)
        # print(self.acceptable_words)

        valid_answer: bool = True

        if len(self.required_words) > 0 and self.required_words[0] != '':
            # print("Checking Requireds")
            for word in self.required_words:
                # print(f"{word} {word in user_answer} {word not in user_answer}")
                if word not in user_answer:
                    # print("Return False")
                    return False
                else: user_answer.remove(word)
        
        if len(self.acceptable_words) > 0 and self.acceptable_words[0] != '':
            # print("Checking Acceptables")
            for word in user_answer:
                # print(f"{word} {word in self.acceptable_words} {word in self.acceptable_words}")
                if word not in self.acceptable_words:
                    # print("Return False")
                    return False

        # print("Return True")
        return True
    
    def create_correct_answer_string(self) -> str:
        return_string: str = self.required_words[0]

        for i in range(1, len(self.required_words)): return_string += f" {self.required_words[i]}"

        return return_string

    def create_dictionary(self) -> dict:
        print(self.is_image_question)
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