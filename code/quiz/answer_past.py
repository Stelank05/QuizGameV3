from questions.answer import Answer

class PastAnswer (Answer):
    def __init__(self, data: list[dict]) -> None:
        Answer.__init__(self, data[0])

        self.display_index: int = self.answer_number
        self.answer_hidden: bool = False
        self.answer_chosen: bool = False

        if len(data) == 2:
            self.display_index = data[1]["Display Index"]
            self.answer_chosen = data[1]["Answer Chosen"]
            self.answer_hidden = data[1]["Answer Hidden"]