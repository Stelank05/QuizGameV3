import re

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from controls.colour_controls import ColourControls
from controls.file_handler import *
from controls.sort_functions import *

from classes.colour import Colour

from common_data import CommonData
from window.window_components import WindowComponents
#from window.window_design import WindowDesign

class TopicControls:
    # Topic Functions

    def select_topic() -> None:
        id_sort_topics(CommonData.topic_list)
        WindowComponents.current_edit_topic = CommonData.topic_list[WindowComponents.topics_listbox.curselection()[0]]
        TopicControls.load_topic_details()

    def create_topic() -> None:
        WindowComponents.topic_back = CommonData.get_colour_from_name(WindowComponents.topic_back_colour.get(), 0, len(CommonData.colour_list))
        WindowComponents.topic_text = CommonData.get_colour_from_name(WindowComponents.topic_text_colour.get(), 0, len(CommonData.colour_list))

        if TopicControls.valid_topic("Create"):
            topic_id: str = TopicControls.generate_topic_id()
            topic_colours: list[str] = [CommonData.get_colour_from_name(WindowComponents.topic_back_colour.get(), 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_name(WindowComponents.topic_text_colour.get(), 0, len(CommonData.colour_list)).colour_id]

            topic_dictionary: dict = {
                "Topic ID": topic_id,
                "Topic Name": WindowComponents.topic_name_entry.get(),
                "Topic Colours": topic_colours
            }

            new_topic: Topic = Topic(topic_dictionary)
            CommonData.topic_list.append(new_topic)

            topic_path: str = os.path.join(CommonData.topics_folder, f"{topic_id}.json")
            write_json_file(topic_path, topic_dictionary)

            TopicControls.update_topic_list()
        else:
            messagebox.showerror("Invalid Topic Data", "Something isn't right, either a non-unique name, or insufficient conrast ratio")

    def update_topic() -> None:
        WindowComponents.topic_back = CommonData.get_colour_from_name(WindowComponents.topic_back_colour.get(), 0, len(CommonData.colour_list))
        WindowComponents.topic_text = CommonData.get_colour_from_name(WindowComponents.topic_text_colour.get(), 0, len(CommonData.colour_list))

        if TopicControls.valid_topic("Update"):
            WindowComponents.current_edit_topic.topic_name = WindowComponents.topic_name_entry.get()
            WindowComponents.current_edit_topic.topic_colours = [CommonData.get_colour_from_name(WindowComponents.topic_back_colour.get(), 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_name(WindowComponents.topic_text_colour.get(), 0, len(CommonData.colour_list)).colour_id]

            topic_path: str = os.path.join(CommonData.topics_folder, f"{WindowComponents.current_edit_topic.topic_id}.json")
            write_json_file(topic_path, WindowComponents.current_edit_topic.make_dictionary())

            TopicControls.update_topic_list()
        else: messagebox.showerror("Invalid Topic Data", "Something isn't right, either a non-unique name, or insufficient conrast ratio")

    def revert_topic() -> None:
        if WindowComponents.current_edit_topic != None: TopicControls.load_topic_details()

    def load_topic_details() -> None:
        TopicControls.clear_edit_topics_page()

        WindowComponents.topic_name_entry.insert(0, WindowComponents.current_edit_topic.topic_name)
        WindowComponents.topic_back_colour.set(CommonData.get_colour_from_id(WindowComponents.current_edit_topic.topic_colours[0], 0, len(CommonData.colour_list)).colour_name)
        WindowComponents.topic_text_colour.set(CommonData.get_colour_from_id(WindowComponents.current_edit_topic.topic_colours[1], 0, len(CommonData.colour_list)).colour_name)

    def valid_topic(check_type: str) -> bool:
        check_name: str = ""

        if check_type == "Update": check_name = WindowComponents.topic_name_entry.get()

        if not TopicControls.unique_topic_name(check_name): return False
        if ColourControls.get_contrast_ratio(WindowComponents.topic_back.luminance, WindowComponents.topic_text.luminance) < WindowComponents.minimum_contrast_ratio: return False
        return True
    
    def unique_topic_name(compare_name: str) -> bool:
        for topic in CommonData.topic_list:
            if compare_name == topic.topic_name and topic != WindowComponents.current_edit_topic: return False
        return True

    def generate_topic_id() -> str:
        if len(CommonData.topic_list) == 0: return "T0001"
        id_sort_topics(CommonData.topic_list)
        return f"T{str(int(CommonData.topic_list[-1].topic_id.replace("T", "")) + 1).rjust(4, "0")}"
    
    def update_topic_list() -> None:
        id_sort_topics(CommonData.topic_list)
        WindowComponents.topics_listbox.delete(0, END)

        for topic in CommonData.topic_list:
            WindowComponents.topics_listbox.insert('end', f"{topic.topic_id} - {topic.topic_name}")

    def clear_topic() -> None:
        WindowComponents.current_edit_topic = None
        TopicControls.clear_edit_topics_page()


    def clear_edit_topics_page() -> None:
        WindowComponents.topic_name_entry.delete(0, len(WindowComponents.topic_name_entry.get()))
        WindowComponents.topic_back_colour.set("")
        WindowComponents.topic_text_colour.set("")
        WindowComponents.contrast_output.configure(text = "Contrast Ratio:\nSomething", bg = WindowComponents.black.colour_code, fg = WindowComponents.white.colour_code)
