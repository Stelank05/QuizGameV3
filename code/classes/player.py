class Player:
    def __init__(self, player_type: str, player_data: dict) -> None:
        self.user_id: str = player_data["User ID"]
        self.username: str = player_data["Username"]
        self.password: str = player_data["Password"]
        self.password_shift: str = player_data["Password Shift"]

        self.player_type: str = player_type

        # User Colours - As ID Codes
        self.window_colours: list[str] = player_data["Colours"]["Window Colours"]
        self.button_colours: list[str] = player_data["Colours"]["Button Colours"]
        self.label_colours: list[str] = player_data["Colours"]["Entry Colours"]
        self.entry_colours: list[str] = player_data["Colours"]["Label Colours"]

        self.high_score: float = float(player_data["High Score"])
        self.previous_attempts: list[str] = player_data["Previous Quizzes"]

    def make_dictionary(self) -> dict:
        return {
            "User ID": self.user_id,
            "Username": self.username,
            "Password": self.password,
            "Password Shift": self.password_shift,
            "Colours": self.make_colour_list(),
            "High Score": self.high_score,
            "Previous Quizzes": self.previous_attempts
        }
    
    def make_colour_list(self) -> dict:
        return {
            "Window Colours" : [self.window_colours[0], self.window_colours[1]],
            "Button Colours" : [self.button_colours[0], self.button_colours[1]],
            "Label Colours" : [self.label_colours[0], self.label_colours[1]],
            "Entry Colours" : [self.entry_colours[0], self.entry_colours[1]]
        }
    
    def display_player(self) -> None:
        print("Details:")
        print(f"User ID: {self.user_id}")
        print(f"Username: {self.username}")
        print(f"Password: REDACTED")
        print(f"Window Colours: {self.window_colours}")
        print(f"Button Colours: {self.button_colours}")
        print(f"Label Colours: {self.label_colours}")
        print(f"Entry Colours: {self.entry_colours}")
        print(f"High Score: {self.high_score}")
        print(f"Previous Quizzes: {self.previous_attempts}")
