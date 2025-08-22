class Guest:
    def __init__(self, guest_data: dict) -> None:
        self.guest_id: str = guest_data["Guest ID"]
        self.username: str = guest_data["Guest Username"]
        
        self.window_colours: list[str] = ["C0024", "C0001"]
        self.label_colours: list[str] = ["C0001", "C0002"]
        self.button_colours: list[str] = ["C0025", "C0002"]
        self.entry_colours: list[str] = ["C0025", "C0002"]
    
    def make_dictionary(self) -> dict:
        return {
            "Guest ID": self.guest_id,
            "Guest Username": self.username
        }