class Audio:
    def __init__(self, audio_data: list[str], full_path: str) -> None:
        self.audio_id: str = audio_data[0]
        self.audio_name: str = audio_data[1]
        self.audio_file: str = audio_data[2]
        self.audio_type: str = audio_data[3]
        self.full_file: str = full_path

    def create_line(self) -> str:
        return f"{self.audio_id},{self.audio_name},{self.audio_file},{self.audio_type}"