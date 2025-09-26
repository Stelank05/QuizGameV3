from tkinter import *

from window.window_components import WindowComponents

class OrderAnswerCreator:
    def __init__(self, frame: Toplevel, answer_number: int, x_start: int, y_start: int) -> None:
        self.include_button: Button = Button(frame, text = answer_number, bg = WindowComponents.entry_colours[1].colour_code, fg = WindowComponents.entry_colours[0].colour_code, font = WindowComponents.main_font, borderwidth = 0, highlightthickness = 0, command = self.toggle_include)
        self.include_button.place(x = x_start, y = y_start, width = 45, height = 30)

        self.answer_input: Entry = Entry(frame, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        self.answer_input.place(x = x_start + 45, y = y_start, width = 130, height = 30)

        self.include_answer: bool = True

    def toggle_include(self) -> None:
        self.include_answer = not self.include_answer

        if self.include_answer:
            self.include_button.configure(bg = WindowComponents.entry_colours[1].colour_code, fg = WindowComponents.entry_colours[0].colour_code)
            self.answer_input.configure(bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code)
        else:
            self.include_button.configure(bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code)
            self.answer_input.configure(bg = WindowComponents.entry_colours[1].colour_code, fg = WindowComponents.entry_colours[0].colour_code)
        
    def clear(self) -> None:
        self.include_button.configure(bg = WindowComponents.entry_colours[1].colour_code, fg = WindowComponents.entry_colours[0].colour_code)
        self.answer_input.delete(0, len(self.answer_input.get()))
        self.answer_input.configure(bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code)