import re

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from classes.colour import Colour

from controls.file_handler import *
from controls.generic_controls import *
from controls.sort_functions import *

from window.window_components import WindowComponents
#from window.window_design import WindowDesign

from common_data import CommonData

class ColourControls:
    def get_contrast_ratio(back_luminance: float, text_luminance: float) -> float:
        if back_luminance > text_luminance: return round(back_luminance / text_luminance, 2)
        return round(text_luminance / back_luminance, 2)

    def check_contrast_ratio(back_luminance: float, text_luminance: float) -> bool:
        ratio: float = ColourControls.get_contrast_ratio(back_luminance, text_luminance)

        if ratio < WindowComponents.minimum_contrast_ratio: return False
        return True

    def update_colour_file() -> None:
        colour_data: str = f"{CommonData.colour_list[0].colour_id},{CommonData.colour_list[0].colour_name},{CommonData.colour_list[0].colour_code},{CommonData.colour_list[0].protected}"

        for i in range(1, len(CommonData.colour_list)): colour_data += f"\n{CommonData.colour_list[i].colour_id},{CommonData.colour_list[i].colour_name},{CommonData.colour_list[i].colour_code},{CommonData.colour_list[i].protected}"

        write_file(CommonData.colour_file, colour_data)


    # Colour Functions - Editing

    def select_colour() -> None:
        id_sort_colours(CommonData.colour_list)
        WindowComponents.current_edit_colour = CommonData.colour_list[WindowComponents.colours_listbox.curselection()[0]]
        ColourControls.load_colour_details()

    def create_colour() -> None:
        colour_code: str = WindowComponents.colour_code_entry.get()
        if colour_code[0] != "#": colour_code = f"#{colour_code}"

        if ColourControls.valid_colour("Create", colour_code):
            colour_id: str = ColourControls.generate_colour_id()
            
            new_colour: Colour = Colour([colour_id, WindowComponents.colour_name_entry.get(), colour_code, "false"])
            CommonData.colour_list.append(new_colour)
            CommonData.colour_names.append(new_colour.colour_name)

            ColourControls.update_colour_list()
            ColourControls.update_colour_file()
        else: messagebox.showerror("Invalid Colour Data", "Something isn't right, either a non-unique name, invalid Hex Code, or something is missing")

    def update_colour() -> None:
        colour_code: str = WindowComponents.colour_code_entry.get()
        if colour_code[0] != "#": colour_code = f"#{colour_code}"

        if ColourControls.valid_colour("Update", colour_code):
            WindowComponents.current_edit_colour.colour_name = WindowComponents.colour_name_entry.get()
            WindowComponents.current_edit_colour.colour_code = colour_code

            ColourControls.update_colour_list()
            ColourControls.update_colour_file()
        else: messagebox.showerror("Invalid Colour Data", "Something isn't right, either a non-unique name, invalid Hex Code, or something is missing")

    def revert_colour() -> None:
        if WindowComponents.current_edit_colour != None: ColourControls.load_colour_details()

    def load_colour_details() -> None:
        ColourControls.clear_edit_colours_page()

        WindowComponents.colour_name_entry.insert(0, WindowComponents.current_edit_colour.colour_name)
        WindowComponents.colour_code_entry.insert(0, WindowComponents.current_edit_colour.colour_code)
        WindowComponents.colour_output.configure(bg = WindowComponents.current_edit_colour.colour_code)

    def valid_colour(check_type: str, colour_code: str) -> bool:
        check_name: str = ""
        if check_type == "Update": check_name = WindowComponents.colour_name_entry.get()

        if not ColourControls.unique_colour_name(check_name): return False
        if not ColourControls.valid_colour_code(colour_code): return False
        if not ColourControls.unique_colour_code(colour_code): return False
        return True

    def unique_colour_name(compare_name: str) -> bool:
        for colour in CommonData.colour_list:
            if compare_name == colour.colour_name and colour != WindowComponents.current_edit_colour: return False
        return True

    def unique_colour_code(compare_code: str) -> bool:
        for colour in CommonData.colour_list:
            if compare_code == colour.colour_code and colour != WindowComponents.current_edit_colour: return False
        return True

    def valid_colour_code(test_code: str) -> bool:
        return bool(re.match(re.compile(r'^#([a-fA-F0-9]{6})$'), test_code))

    def generate_colour_id() -> str:
        if len(CommonData.colour_list) == 0: return "C0001"
        id_sort_colours(CommonData.colour_list)
        return f"C{str(int(CommonData.colour_list[-1].colour_id.replace("C", "")) + 1).rjust(4, "0")}"

    def update_colour_list() -> None:
        id_sort_colours(CommonData.colour_list)
        WindowComponents.colours_listbox.delete(0, END)

        for colour in CommonData.colour_list: WindowComponents.colours_listbox.insert('end', f"{colour.colour_id} - {colour.colour_name}")

    def set_colour_output() -> None:
        colour_code: str = WindowComponents.colour_code_entry.get()

        if colour_code != "":
            if colour_code[0] != "#": colour_code = f"#{colour_code}"

            valid_code: bool = ColourControls.valid_colour_code(colour_code)
            if valid_code: WindowComponents.colour_output.configure(bg = colour_code)
        else: messagebox.showerror("ERROR", "No Colour Hex Code Entered")

    def clear_colour() -> None:
        WindowComponents.current_edit_colour = None
        ColourControls.clear_edit_colours_page()


    # Colour Functions - Account
    #   Selection Functions

    def reset_colour_options(selector_type: str) -> None:
        set_back: str; set_text: str

        [set_back, set_text] = ColourControls.get_set_colours(selector_type, "Window")
        WindowComponents.window_back.set(set_back.colour_name)
        WindowComponents.window_text.set(set_text.colour_name)

        [set_back, set_text] = ColourControls.get_set_colours(selector_type, "Button")
        WindowComponents.button_back.set(set_back.colour_name)
        WindowComponents.button_text.set(set_text.colour_name)

        [set_back, set_text] = ColourControls.get_set_colours(selector_type, "Label")
        WindowComponents.label_back.set(set_back.colour_name)
        WindowComponents.label_text.set(set_text.colour_name)

        [set_back, set_text] = ColourControls.get_set_colours(selector_type, "Entry")
        WindowComponents.entry_back.set(set_back.colour_name)
        WindowComponents.entry_text.set(set_text.colour_name)

    def select_colours(frame: Toplevel, selector_type: str) -> None:
        if selector_type == "Create Account":
            WindowComponents.chosen_window_back = CommonData.get_colour_from_name(WindowComponents.window_back.get(), 0, len(CommonData.colour_list))
            WindowComponents.chosen_window_text = CommonData.get_colour_from_name(WindowComponents.window_text.get(), 0, len(CommonData.colour_list))
            WindowComponents.chosen_button_back = CommonData.get_colour_from_name(WindowComponents.button_back.get(), 0, len(CommonData.colour_list))
            WindowComponents.chosen_button_text = CommonData.get_colour_from_name(WindowComponents.button_text.get(), 0, len(CommonData.colour_list))
            WindowComponents.chosen_label_back = CommonData.get_colour_from_name(WindowComponents.label_back.get(), 0, len(CommonData.colour_list))
            WindowComponents.chosen_label_text = CommonData.get_colour_from_name(WindowComponents.label_text.get(), 0, len(CommonData.colour_list))
            WindowComponents.chosen_entry_back = CommonData.get_colour_from_name(WindowComponents.entry_back.get(), 0, len(CommonData.colour_list))
            WindowComponents.chosen_entry_text = CommonData.get_colour_from_name(WindowComponents.entry_text.get(), 0, len(CommonData.colour_list))

            winbut_ratio: float = ColourControls.get_contrast_ratio(WindowComponents.chosen_window_back.luminance, WindowComponents.chosen_button_back.luminance)
            winlab_ratio: float = ColourControls.get_contrast_ratio(WindowComponents.chosen_window_back.luminance, WindowComponents.chosen_label_back.luminance)
            winent_ratio: float = ColourControls.get_contrast_ratio(WindowComponents.chosen_window_back.luminance, WindowComponents.chosen_entry_back.luminance)

            winbut_ratio_str: str = f"Button Colours\n{winbut_ratio}:1"
            winlab_ratio_str: str = f"Label Colours\n{winlab_ratio}:1"
            winent_ratio_str: str = f"Entry Colours\n{winent_ratio}:1"

            if winbut_ratio < WindowComponents.minimum_contrast_ratio: winbut_ratio_str += " !!"
            if winlab_ratio < WindowComponents.minimum_contrast_ratio: winlab_ratio_str += " !!"
            if winent_ratio < WindowComponents.minimum_contrast_ratio: winent_ratio_str += " !!"

            WindowComponents.background_display.configure(bg = WindowComponents.chosen_window_back.colour_code, fg = WindowComponents.chosen_window_text.colour_code)
            WindowComponents.window_display.configure(bg = WindowComponents.chosen_window_back.colour_code, fg = WindowComponents.chosen_window_text.colour_code)
            WindowComponents.button_display.configure(text = winbut_ratio_str, bg = WindowComponents.chosen_button_back.colour_code, fg = WindowComponents.chosen_button_text.colour_code)
            WindowComponents.label_display.configure(text = winlab_ratio_str, bg = WindowComponents.chosen_label_back.colour_code, fg = WindowComponents.chosen_label_text.colour_code)
            WindowComponents.entry_display.configure(text = winent_ratio_str, bg = WindowComponents.chosen_entry_back.colour_code, fg = WindowComponents.chosen_entry_text.colour_code)

        elif selector_type == "Update User Colours":
            current_window_colours: list[Colour] = [CommonData.get_colour_from_name(WindowComponents.window_back.get(), 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_name(WindowComponents.window_text.get(), 0, len(CommonData.colour_list)).colour_id]
            current_button_colours: list[Colour] = [CommonData.get_colour_from_name(WindowComponents.button_back.get(), 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_name(WindowComponents.button_text.get(), 0, len(CommonData.colour_list)).colour_id]
            current_label_colours: list[Colour] = [CommonData.get_colour_from_name(WindowComponents.label_back.get(), 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_name(WindowComponents.label_text.get(), 0, len(CommonData.colour_list)).colour_id]
            current_entry_colours: list[Colour] = [CommonData.get_colour_from_name(WindowComponents.entry_back.get(), 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_name(WindowComponents.entry_text.get(), 0, len(CommonData.colour_list)).colour_id]

            WindowComponents.window_colours = get_colours(current_window_colours)
            WindowComponents.button_colours = get_colours(current_button_colours)
            WindowComponents.label_colours = get_colours(current_label_colours)
            WindowComponents.entry_colours = get_colours(current_entry_colours)

            winbut_ratio: float = ColourControls.get_contrast_ratio(WindowComponents.window_colours[0].luminance, WindowComponents.button_colours[0].luminance)
            winlab_ratio: float = ColourControls.get_contrast_ratio(WindowComponents.window_colours[0].luminance, WindowComponents.label_colours[0].luminance)
            winent_ratio: float = ColourControls.get_contrast_ratio(WindowComponents.window_colours[0].luminance, WindowComponents.entry_colours[0].luminance)

            winbut_ratio_str: str = f"Button Colours\n{winbut_ratio}:1"
            winlab_ratio_str: str = f"Label Colours\n{winlab_ratio}:1"
            winent_ratio_str: str = f"Entry Colours\n{winent_ratio}:1"

            if winbut_ratio < WindowComponents.minimum_contrast_ratio: winbut_ratio_str += " !!"
            if winlab_ratio < WindowComponents.minimum_contrast_ratio: winlab_ratio_str += " !!"
            if winent_ratio < WindowComponents.minimum_contrast_ratio: winent_ratio_str += " !!"

            WindowComponents.ua_background_display.configure(bg = WindowComponents.window_colours[0].colour_code, fg = WindowComponents.window_colours[1].colour_code)
            WindowComponents.ua_window_display.configure(bg = WindowComponents.window_colours[0].colour_code, fg = WindowComponents.window_colours[1].colour_code)
            WindowComponents.ua_button_display.configure(text = winbut_ratio_str, bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
            WindowComponents.ua_label_display.configure(text = winlab_ratio_str, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code)
            WindowComponents.ua_entry_display.configure(text = winent_ratio_str, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code)
        
        frame.withdraw()

    def valid_colours() -> bool:
        win_back: Colour = WindowComponents.chosen_window_back; win_text: Colour = WindowComponents.chosen_window_text
        but_back: Colour = WindowComponents.chosen_button_back; but_text: Colour = WindowComponents.chosen_button_text
        lab_back: Colour = WindowComponents.chosen_label_back; lab_text: Colour = WindowComponents.chosen_label_text
        ent_back: Colour = WindowComponents.chosen_entry_back; ent_text: Colour = WindowComponents.chosen_entry_text
    
        for colour in WindowComponents.chosen_colours:
            if colour == None: return False

        if ColourControls.get_contrast_ratio(win_back.luminance, win_text.luminance) < WindowComponents.minimum_contrast_ratio: return False
        if ColourControls.get_contrast_ratio(but_back.luminance, but_text.luminance) < WindowComponents.minimum_contrast_ratio: return False
        if ColourControls.get_contrast_ratio(lab_back.luminance, lab_text.luminance) < WindowComponents.minimum_contrast_ratio: return False
        if ColourControls.get_contrast_ratio(ent_back.luminance, ent_text.luminance) < WindowComponents.minimum_contrast_ratio: return False
        if ColourControls.get_contrast_ratio(win_back.luminance, but_back.luminance) < WindowComponents.minimum_contrast_ratio: return False
        if ColourControls.get_contrast_ratio(win_back.luminance, lab_back.luminance) < WindowComponents.minimum_contrast_ratio: return False
        if ColourControls.get_contrast_ratio(win_back.luminance, ent_back.luminance) < WindowComponents.minimum_contrast_ratio: return False

        return True

    #   Contrast Controls

    def set_contrast_ratio(colour_set: str, contrast_label: Label) -> None:
        back_colour: Colour
        text_colour: Colour

        match colour_set:
            case "Window":
                back_colour = CommonData.get_colour_from_name(WindowComponents.window_back.get(), 0, len(CommonData.colour_list))
                text_colour = CommonData.get_colour_from_name(WindowComponents.window_text.get(), 0, len(CommonData.colour_list))
            case "Button":
                back_colour = CommonData.get_colour_from_name(WindowComponents.button_back.get(), 0, len(CommonData.colour_list))
                text_colour = CommonData.get_colour_from_name(WindowComponents.button_text.get(), 0, len(CommonData.colour_list))
            case "Label":
                back_colour = CommonData.get_colour_from_name(WindowComponents.label_back.get(), 0, len(CommonData.colour_list))
                text_colour = CommonData.get_colour_from_name(WindowComponents.label_text.get(), 0, len(CommonData.colour_list))
            case "Entry":
                back_colour = CommonData.get_colour_from_name(WindowComponents.entry_back.get(), 0, len(CommonData.colour_list))
                text_colour = CommonData.get_colour_from_name(WindowComponents.entry_text.get(), 0, len(CommonData.colour_list))
            case "Topics":
                back_colour = CommonData.get_colour_from_name(WindowComponents.topic_back_colour.get(), 0, len(CommonData.colour_list))
                text_colour = CommonData.get_colour_from_name(WindowComponents.topic_text_colour.get(), 0, len(CommonData.colour_list))

        if type(back_colour) != Colour or type(text_colour) != Colour:
            messagebox.showerror("No Colour Selected", "You Are Missing a Colour Option")
            return 0

        contrast_label.configure(text = f"Contrast Ratio:\n{ColourControls.get_contrast_ratio(back_colour.luminance, text_colour.luminance)}:1", bg = back_colour.colour_code, fg = text_colour.colour_code)

    def set_contrast_ratio_answer(back_colour: StringVar, text_colour: StringVar, label: Label) -> None:
        background: Colour = CommonData.get_colour_from_name(back_colour.get(), 0, len(CommonData.colour_list))
        foreground: Colour = CommonData.get_colour_from_name(text_colour.get(), 0, len(CommonData.colour_list))

        if type(background) != Colour or type(foreground) != Colour:
            messagebox.showerror("No Colour Selected", "You Are Missing a Colour Option")
            return 0

        label.configure(text = f"Contrast Ratio:\n{ColourControls.get_contrast_ratio(background.luminance, foreground.luminance)}:1", bg = background.colour_code, fg = foreground.colour_code)

    def get_set_colours(selector_type: str, header: str) -> list[Colour]:
        return_back: str; return_text: str

        if selector_type == "Create Account":
            match header:
                case "Window":
                    return_back = WindowComponents.window_colours[0]
                    return_text = WindowComponents.window_colours[1]
                    return [return_back, return_text]
                case "Button":
                    return_back = WindowComponents.button_colours[0]
                    return_text = WindowComponents.button_colours[1]
                    return [return_back, return_text]
                case "Label":
                    return_back = WindowComponents.label_colours[0]
                    return_text = WindowComponents.label_colours[1]
                    return [return_back, return_text]
                case "Entry":
                    return_back = WindowComponents.entry_colours[0]
                    return_text = WindowComponents.entry_colours[1]
                    return [return_back, return_text]
        elif selector_type == "Update User Colours":
            match header:
                case "Window":
                    return_back = CommonData.get_colour_from_id(WindowComponents.active_user.window_colours[0], 0, len(CommonData.colour_list))
                    return_text = CommonData.get_colour_from_id(WindowComponents.active_user.window_colours[1], 0, len(CommonData.colour_list))
                    return [return_back, return_text]
                case "Button":
                    return_back = CommonData.get_colour_from_id(WindowComponents.active_user.button_colours[0], 0, len(CommonData.colour_list))
                    return_text = CommonData.get_colour_from_id(WindowComponents.active_user.button_colours[1], 0, len(CommonData.colour_list))
                    return [return_back, return_text]
                case "Label":
                    return_back = CommonData.get_colour_from_id(WindowComponents.active_user.label_colours[0], 0, len(CommonData.colour_list))
                    return_text = CommonData.get_colour_from_id(WindowComponents.active_user.label_colours[1], 0, len(CommonData.colour_list))
                    return [return_back, return_text]
                case "Entry":
                    return_back = CommonData.get_colour_from_id(WindowComponents.active_user.entry_colours[0], 0, len(CommonData.colour_list))
                    return_text = CommonData.get_colour_from_id(WindowComponents.active_user.entry_colours[1], 0, len(CommonData.colour_list))
                    return [return_back, return_text]


    #   Set Active Colours

    def set_user_colours() -> None:
        WindowComponents.window_colours = get_colours(WindowComponents.active_user.window_colours)
        WindowComponents.button_colours = get_colours(WindowComponents.active_user.button_colours)
        WindowComponents.label_colours = get_colours(WindowComponents.active_user.label_colours)
        WindowComponents.entry_colours = get_colours(WindowComponents.active_user.entry_colours)

    def reset_colours() -> None:
        WindowComponents.window_colours = WindowComponents.default_window_colours
        WindowComponents.button_colours = WindowComponents.default_button_colours
        WindowComponents.label_colours = WindowComponents.default_label_colours
        WindowComponents.entry_colours = WindowComponents.default_entry_colours

    def clear_edit_colours_page() -> None:
        WindowComponents.colour_name_entry.delete(0, len(WindowComponents.colour_name_entry.get()))
        WindowComponents.colour_code_entry.delete(0, len(WindowComponents.colour_code_entry.get()))
        WindowComponents.colour_output.configure(bg = WindowComponents.black.colour_code)
