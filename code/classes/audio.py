class Audio:
    def __init__(self, audio_data: list[str], full_path: str) -> None:
        self.audio_id: str = audio_data[0]
        self.audio_name: str = audio_data[1]
        self.audio_file: str = audio_data[2]
        self.full_file: str = full_path