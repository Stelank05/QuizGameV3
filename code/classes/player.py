class Player:
    def __init__(self, player_data: dict) -> None:
        self.user_id: str = player_data["User ID"]
        self.username: str = player_data["Username"]
        self.password: str = player_data["Password"]
        self.password_shift: str = player_data["Password Shift"]

        # self.player_type: str = player_type

        # User Colours - As ID Codes
        self.window_colours: list[str] = player_data["Colours"]["Window Colours"]
        self.button_colours: list[str] = player_data["Colours"]["Button Colours"]
        self.label_colours: list[str] = player_data["Colours"]["Label Colours"]
        self.entry_colours: list[str] = player_data["Colours"]["Entry Colours"]

        self.high_score: float = float(player_data["High Score"])
        self.high_score_percentage: float = float(player_data["High Score Percentage"])

        self.previous_attempts: list[str] = []
        for attempt in player_data["Previous Quizzes"]: self.previous_attempts.append(attempt)

        # Leaderboard Settings
        self.hide_max_score: bool = player_data["Leaderboard Settings"]["Hide Max Score"]
        self.hide_score_percentage: bool = player_data["Leaderboard Settings"]["Hide Score Percentage"]
        self.hide_incorrect_count: bool = player_data["Leaderboard Settings"]["Hide Incorrect Count"]
        self.hide_questions_percentage: bool = player_data["Leaderboard Settings"]["Hide Question Percentage"]
        self.hide_hint_breakdown: bool = player_data["Leaderboard Settings"]["Hide Hint Breakdown"]

    def make_dictionary(self) -> dict:
        return {
            "User ID": self.user_id,
            "Username": self.username,
            "Password": self.password,
            "Password Shift": self.password_shift,
            "Colours": self.make_colour_list(),
            "High Score": self.high_score,
            "High Score Percentage": self.high_score_percentage,
            "Previous Quizzes": self.previous_attempts,
            "Leaderboard Settings": self.make_settings_dict()
        }

    def make_colour_list(self) -> dict:
        return {
            "Window Colours" : [self.window_colours[0], self.window_colours[1]],
            "Button Colours" : [self.button_colours[0], self.button_colours[1]],
            "Label Colours" : [self.label_colours[0], self.label_colours[1]],
            "Entry Colours" : [self.entry_colours[0], self.entry_colours[1]]
        }
    
    def make_settings_dict(self) -> dict:
        return {
            "Hide Max Score": self.hide_max_score,
            "Hide Score Percentage": self.hide_score_percentage,
            "Hide Incorrect Count": self.hide_incorrect_count,
            "Hide Question Percentage": self.hide_questions_percentage,
            "Hide Hint Breakdown": self.hide_hint_breakdown
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
