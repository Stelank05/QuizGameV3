from tkinter import *
from tkinter import messagebox

from classes.colour import Colour

from common_data import CommonData

def exit_app(window: Tk):
    window.destroy()

def destroy_all_pages(pages: list[Toplevel]):
    for page in pages:
        page.destroy()

def get_colours(colour_ids: list[str]) -> list[Colour]:
#    print(colour_ids[0], colour_ids[1])
    back_colour: Colour = CommonData.get_colour_from_id(colour_ids[0], 0, len(CommonData.colour_list))
    text_colour: Colour = CommonData.get_colour_from_id(colour_ids[1], 0, len(CommonData.colour_list))

    return [back_colour, text_colour]