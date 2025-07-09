class Topic:
    def __init__(self, topic_data: dict) -> None:
        self.topic_id: str = topic_data["Topic ID"]
        self.topic_name: str = topic_data["Topic Name"]
        self.topic_colours: list[str] = topic_data["Topic Colours"]
        
        self.questions: list[str] = []
        self.total_questions: int = 0

    def make_dictionary(self) -> dict:
        return {
            "Topic ID": self.topic_id,
            "Topic Name": self.topic_name,
            "Topic Colours": self.topic_colours
        }