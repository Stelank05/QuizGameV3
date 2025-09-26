import functools
from tkinter import *
from tkinter import ttk

from classes.colour import Colour
from controls.colour_controls import ColourControls

from window.window_components import WindowComponents

from common_data import CommonData

class ClosedAnswerCreator:
    def __init__(self, frame: Toplevel, answer_number: int, x_value: int) -> None:
        self.answer_number: int = answer_number

        self.correct_answer: bool = False
        self.include_answer: bool = True

        if answer_number == 1: self.correct_answer = True

        self.header_label: Label = Label(frame, text = f"Answer {answer_number}", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        self.header_label.place(x = x_value, y = 235, width = 175, height = 30)

        self.answer_entry: Text = Text(frame, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        self.answer_entry.place(x = x_value, y = 270, width = 175, height = 65)

        self.selected_background: StringVar = StringVar()
        self.selected_foreground: StringVar = StringVar()

        self.background: ttk.Combobox = ttk.Combobox(frame)
        self.background['values'] = CommonData.colour_names
        self.background['state'] = 'readonly'
        self.background.place(x = x_value, y = 340, width = 175, height = 30)
        self.background.configure(textvariable = self.selected_background)
        self.background.set("Background Colour")

        self.foreground: ttk.Combobox = ttk.Combobox(frame)
        self.foreground['values'] = CommonData.colour_names
        self.foreground['state'] = 'readonly'
        self.foreground.place(x = x_value, y = 375, width = 175, height = 30)
        self.foreground.configure(textvariable = self.selected_foreground)
        self.foreground.set("Text Colour")

        self.output_label: Label = Label(frame, text = "Contrast Ratio: Something", wraplength = 130, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        self.output_label.place(x = x_value, y = 410, width = 175, height = 45)

        self.preview_button: Button = Button(frame, text = "Calculate Colour Contrast Ratio", wraplength = 130, bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(ColourControls.set_contrast_ratio_answer, self.selected_background, self.selected_foreground, self.output_label))
        self.preview_button.place(x = x_value, y = 460, width = 175, height = 45)

        self.is_correct_answer: Button = Button(frame, text = f"Correct Answer: {self.correct_answer}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = self.toggle_is_correct)
        self.is_correct_answer.place(x = x_value, y = 510, width = 175, height = 30)

        if self.correct_answer: self.is_correct_answer.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

        self.include_button: Button = Button(frame, text = f"Include Answer: {self.include_answer}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = self.toggle_inclusion)
        self.include_button.place(x = x_value, y = 545, width = 175, height = 30)

    def toggle_is_correct(self) -> None:
        self.correct_answer = not self.correct_answer

        self.is_correct_answer.configure(text = f"Correct Answer: {self.correct_answer}")

        if self.correct_answer: self.is_correct_answer.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: self.is_correct_answer.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

    def toggle_inclusion(self) -> None:
        self.include_answer = not self.include_answer

        self.include_button.configure(text = f"Include Answer: {self.include_answer}")

        if self.include_answer: self.include_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        else: self.include_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

    def valid_answer(self) -> bool:
        if self.correct_answer and not self.include_answer: return False
        
        if self.answer_entry.get("1.0", END).strip()[:-1] == "": return False

        if self.background.get() not in CommonData.colour_names: return False
        if self.foreground.get() not in CommonData.colour_names: return False

        back_colour: Colour = CommonData.get_colour_from_name(self.background.get(), 0, len(CommonData.colour_list))
        text_colour: Colour = CommonData.get_colour_from_name(self.foreground.get(), 0, len(CommonData.colour_list))
        if not ColourControls.check_contrast_ratio(back_colour.luminance, text_colour.luminance): return False

        return True
    
    def clear(self) -> None:
        self.correct_answer: bool = False
        self.include_answer: bool = True

        self.answer_entry.delete("1.0", END)

        if self.answer_number == 1: self.correct_answer = True

        if self.correct_answer: self.is_correct_answer.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: self.is_correct_answer.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

        self.is_correct_answer.configure(text = f"Correct Answer: {self.correct_answer}")

        self.background.set("Background Colour")
        self.foreground.set("Text Colour")
        
        self.output_label.configure(text = "Contrast Ratio: Something", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code)
        self.include_button.configure(text = f"Include Answer: {self.include_answer}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)