from tkinter import *

from classes.colour import Colour
from classes.guest import Guest
from classes.player import Player

from quiz.quiz_past import PastQuiz

from common_data import CommonData

class LeaderboardRow:
    def __init__(self, window: Toplevel, label_colours: list[str], button_colours: list[Colour], main_font: tuple[str, int], y_position: int) -> None:
        self.position: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.position.place(x = 25, y = y_position, width = 60, height = 30)

        self.username: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.username.place(x = 90, y = y_position, width = 150, height = 30)

        self.quiz_length: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.quiz_length.place(x = 245, y = y_position, width = 120, height = 30)
        

        self.score_achieved: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.score_achieved.place(x = 370, y = y_position, width = 50, height = 30)

        self.score_theoretical: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.score_theoretical.place(x = 420, y = y_position, width = 50, height = 30)

        self.score_percentage: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.score_percentage.place(x = 470, y = y_position, width = 70, height = 30)


        self.correct: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.correct.place(x = 545, y = y_position, width = 85, height = 30)

        self.incorrect: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.incorrect.place(x = 630, y = y_position, width = 85, height = 30)

        self.correct_percentage: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.correct_percentage.place(x = 715, y = y_position, width = 85, height = 30)


        self.hints_total: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.hints_total.place(x = 805, y = y_position, width = 65, height = 30)

        self.hints_text: Label = Label(window, bg = label_colours[1], fg = label_colours[0], font = main_font)
        self.hints_text.place(x = 870, y = y_position, width = 65, height = 30)

        self.hints_closed: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.hints_closed.place(x = 935, y = y_position, width = 65, height = 30)

        self.hints_open: Label = Label(window, bg = label_colours[1], fg = label_colours[0], font = main_font)
        self.hints_open.place(x = 1000, y = y_position, width = 65, height = 30)

        self.hints_order: Label = Label(window, bg = label_colours[0], fg = label_colours[1], font = main_font)
        self.hints_order.place(x = 1065, y = y_position, width = 65, height = 30)

        self.review_button: Button = Button(window, bg = button_colours[0].colour_code, fg = button_colours[1].colour_code, font = main_font)
        self.review_button.place(x = 1135, y = y_position, width = 100, height = 30)

    def set_quiz(self, quiz: PastQuiz, pos: str = "P-") -> None:
        self.position.configure(text = pos)

        player: Player | Guest

        if quiz.player_id[0] == "U": player = CommonData.get_account_from_id(quiz.player_id, 0, len(CommonData.players))
        else: player = CommonData.get_guest_from_id(quiz.player_id, 0, len(CommonData.guests))

        self.username.configure(text = player.username)
        self.quiz_length.configure(text = f"{len(quiz.questions)} Questions")
        
        self.score_achieved.configure(text = quiz.score)
        self.score_theoretical.configure(text = quiz.max_score)
        self.score_percentage.configure(text = f"{quiz.percentage}%")

        self.correct.configure(text = f"{quiz.correct_count} Correct")
        self.incorrect.configure(text = f"{quiz.incorrect_count} Incorrect")
        self.correct_percentage.configure(text = f"{quiz.correct_percentage} %")

        self.hints_total.configure(text = f"Tot: {quiz.total_hints_used}")
        self.hints_text.configure(text = f"Txt: {quiz.text_hints_used}")
        self.hints_closed.configure(text = f"Clo: {quiz.closed_hints_used}")
        self.hints_open.configure(text = f"Opn: {quiz.open_hints_used}")
        self.hints_order.configure(text = f"Ord: {quiz.order_hints_used}")

        self.review_button.configure(text = f"Review Quiz")

    def clear_quiz(self) -> None:
        self.position.configure(text = "P-")

        self.username.configure(text = "")
        self.quiz_length.configure(text = "")
        
        self.score_achieved.configure(text = "")
        self.score_theoretical.configure(text = "")
        self.score_percentage.configure(text = "")

        self.correct.configure(text = "")
        self.incorrect.configure(text = "")
        self.correct_percentage.configure(text = "")

        self.hints_total.configure(text = "")
        self.hints_text.configure(text = "")
        self.hints_closed.configure(text = "")
        self.hints_open.configure(text = "")
        self.hints_order.configure(text = "")

        self.review_button.configure(text = "")