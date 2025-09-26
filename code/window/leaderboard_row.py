from tkinter import *

from classes.colour import Colour
from classes.guest import Guest
from classes.player import Player

from quiz.quiz_past import PastQuiz

from common_data import CommonData

class LeaderboardRow:
    def __init__(self, window: Toplevel, player: Player, label_colours: list[str], button_colours: list[Colour], main_font: tuple[str, int], y_position: int) -> None:
        self.position: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.position.place(x = 25, y = y_position, width = 60, height = 30)

        self.username: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.username.place(x = 90, y = y_position, width = 150, height = 30)

        self.quiz_length: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.quiz_length.place(x = 245, y = y_position, width = 120, height = 30)
        
        x_value: int = 470

        self.score_achieved: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.score_achieved.place(x = 370, y = y_position, width = 50, height = 30)

        self.score_theoretical: Label = None
        self.score_separator: Label = None
        self.score_percentage: Label = None

        if player.hide_max_score:
            x_value = 420
        else:
            self.score_theoretical = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
            self.score_theoretical.place(x = 420, y = y_position, width = 50, height = 30)

            self.score_separator = Label(window, text = "/", bg = label_colours[0], fg = label_colours[1], font = main_font)
            self.score_separator.place(x = 410, y = y_position, width = 20, height = 30)

        if not player.hide_score_percentage:
            self.score_percentage = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
            self.score_percentage.place(x = x_value, y = y_position, width = 70, height = 30)
            x_value += 75
        else: x_value += 5

        self.correct: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.correct.place(x = x_value, y = y_position, width = 85, height = 30)
        x_value += 85
        
        self.incorrect: Label = None

        if not player.hide_incorrect_count:
            self.incorrect: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
            self.incorrect.place(x = x_value, y = y_position, width = 85, height = 30)
            x_value += 85

        if not player.hide_questions_percentage:
            self.correct_percentage: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
            self.correct_percentage.place(x = x_value, y = y_position, width = 85, height = 30)
            x_value += 90
        else: x_value += 5


        self.hints_total: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.hints_total.place(x = x_value, y = y_position, width = 65, height = 30)

        if not player.hide_hint_breakdown:
            x_value += 65
            
            self.hints_text: Label = Label(window, bg = label_colours[1], fg = label_colours[0], font = main_font)
            self.hints_text.place(x = x_value, y = y_position, width = 65, height = 30)
            x_value += 65

            self.hints_closed: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
            self.hints_closed.place(x = x_value, y = y_position, width = 65, height = 30)
            x_value += 65

            self.hints_open: Label = Label(window, bg = label_colours[1], fg = label_colours[0], font = main_font)
            self.hints_open.place(x = x_value, y = y_position, width = 65, height = 30)
            x_value += 65

            self.hints_order: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
            self.hints_order.place(x = x_value, y = y_position, width = 65, height = 30)
            x_value += 70
        else:
            self.hints_total.place(width = 100)
            x_value += 105


        self.review_button: Button = Button(window, bg = button_colours[0].colour_code, fg = button_colours[1].colour_code, font = main_font)
        self.review_button.place(x = x_value, y = y_position, width = 100, height = 30)

    def set_quiz(self, quiz: PastQuiz, player: Player, pos: str = "P-") -> None:
        self.position.configure(text = pos)

        player: Player | Guest

        if quiz.player_id[0] == "U":
            self.username.configure(text = CommonData.get_account_from_id(quiz.player_id, 0, len(CommonData.players)).username)
        else:
            self.username.configure(text = CommonData.get_guest_from_id(quiz.player_id, 0, len(CommonData.guests)).username)
        
        self.quiz_length.configure(text = f"{len(quiz.questions)} Questions")
        
        self.score_achieved.configure(text = quiz.score)
        if not player.hide_max_score:
            self.score_theoretical.configure(text = quiz.max_score)
        if not player.hide_score_percentage:
            self.score_percentage.configure(text = f"{quiz.percentage}%")

        self.correct.configure(text = f"{quiz.correct_count} Correct")

        if not player.hide_incorrect_count:
            self.incorrect.configure(text = f"{quiz.incorrect_count} Incorrect")

        if not player.hide_questions_percentage:
            self.correct_percentage.configure(text = f"{quiz.correct_percentage} %")

        self.hints_total.configure(text = f"Tot: {quiz.total_hints_used}")
        
        if not player.hide_hint_breakdown:
            self.hints_text.configure(text = f"Txt: {quiz.text_hints_used}")
            self.hints_closed.configure(text = f"Clo: {quiz.closed_hints_used}")
            self.hints_open.configure(text = f"Opn: {quiz.open_hints_used}")
            self.hints_order.configure(text = f"Ord: {quiz.order_hints_used}")
        else: self.hints_total.configure(text = f"Total: {quiz.total_hints_used}")
        

        self.review_button.configure(text = f"Review Quiz")

    def clear_quiz(self, player: Player) -> None:
        self.position.configure(text = "P-")

        self.username.configure(text = "")
        self.quiz_length.configure(text = "")
        
        self.score_achieved.configure(text = "")
        if not player.hide_max_score: self.score_theoretical.configure(text = "")
        if not player.hide_score_percentage: self.score_percentage.configure(text = "")

        self.correct.configure(text = "")
        
        if not player.hide_incorrect_count: self.incorrect.configure(text = "")
        if not player.hide_questions_percentage: self.correct_percentage.configure(text = "")

        self.hints_total.configure(text = "")

        if not player.hide_hint_breakdown:
            self.hints_text.configure(text = "")
            self.hints_closed.configure(text = "")
            self.hints_open.configure(text = "")
            self.hints_order.configure(text = "")

        self.review_button.configure(text = "", command = LeaderboardRow.xyz)
    
    def xyz() -> None: pass