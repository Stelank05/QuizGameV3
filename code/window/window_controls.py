import functools
import PIL.Image
import PIL.ImageTk

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from classes.colour import Colour

from controls.audio_controls import AudioControls
from controls.colour_controls import ColourControls
from controls.generic_controls import *
from controls.player_controls import *
from controls.question_controller import QuestionController
from controls.sort_functions import *
from controls.topic_controls import TopicControls

from questions.question_base import BaseQuestion
from questions.question_closed import ClosedQuestion
from questions.question_open import OpenQuestion
from questions.question_order import OrderQuestion

from window.window_components import WindowComponents

from common_data import CommonData

class WindowControls:
    def setup_window(window_: Tk) -> None:
        WindowComponents.window = window_
        
        WindowComponents.default_window_colours = get_colours(WindowComponents.window_colours)
        WindowComponents.default_button_colours = get_colours(WindowComponents.button_colours)
        WindowComponents.default_label_colours = get_colours(WindowComponents.label_colours)
        WindowComponents.default_entry_colours = get_colours(WindowComponents.entry_colours)

        WindowComponents.window_colours = WindowComponents.default_window_colours
        WindowComponents.button_colours = WindowComponents.default_button_colours
        WindowComponents.label_colours = WindowComponents.default_label_colours
        WindowComponents.entry_colours = WindowComponents.default_entry_colours

        #WindowComponents.font = WindowComponents.main_font

        WindowComponents.window_colour_widgets = []
        WindowComponents.button_colour_widgets = []
        WindowComponents.label_colour_widgets = []
        WindowComponents.entry_colour_widgets = []

        WindowComponents.black = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list))
        WindowComponents.white = CommonData.get_colour_from_name("White", 0, len(CommonData.colour_list))

        #WindowControls.create_login_page()
        #WindowComponents.window.mainloop()
 

    # Account Functions
        
    def revert_account() -> None:
        WindowControls.clear_edit_accounts_page()

        WindowComponents.choose_colours.destroy()

        current_window_colours: list[Colour] = [CommonData.get_colour_from_id(WindowComponents.active_user.window_colours[0], 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_id(WindowComponents.active_user.window_colours[1], 0, len(CommonData.colour_list)).colour_id]
        current_button_colours: list[Colour] = [CommonData.get_colour_from_id(WindowComponents.active_user.button_colours[0], 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_id(WindowComponents.active_user.button_colours[1], 0, len(CommonData.colour_list)).colour_id]
        current_label_colours: list[Colour] = [CommonData.get_colour_from_id(WindowComponents.active_user.label_colours[0], 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_id(WindowComponents.active_user.label_colours[1], 0, len(CommonData.colour_list)).colour_id]
        current_entry_colours: list[Colour] = [CommonData.get_colour_from_id(WindowComponents.active_user.entry_colours[0], 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_id(WindowComponents.active_user.entry_colours[1], 0, len(CommonData.colour_list)).colour_id]

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

        WindowComponents.update_username_entry.insert(0, WindowComponents.active_user.username)
        WindowComponents.update_password_entry.insert(0, decrypyt_password(WindowComponents.active_user.password, WindowComponents.active_user.password_shift))

    def jsonify_user_data() -> dict:
        [encrypted_password, shift_key] = encrypt_password(WindowComponents.create_password_entry.get())

        return {
            "User ID": generate_user_id(),
            "Username": WindowComponents.create_username_entry.get(),
            "Password": encrypted_password,
            "Password Shift": shift_key,
            "Colours": WindowControls.make_colour_list(),
            "High Score": 0,
            "Previous Quizzes": []
        }
    
    def make_colour_list() -> dict:
        return {
            "Window Colours" : [WindowComponents.chosen_window_back.colour_id, WindowComponents.chosen_window_text.colour_id],
            "Button Colours" : [WindowComponents.chosen_button_back.colour_id, WindowComponents.chosen_button_text.colour_id],
            "Label Colours" : [WindowComponents.chosen_label_back.colour_id, WindowComponents.chosen_label_text.colour_id],
            "Entry Colours" : [WindowComponents.chosen_entry_back.colour_id, WindowComponents.chosen_entry_text.colour_id],
        }


    # Question Functions

    def display_questions() -> None:
        if not WindowComponents.display_all and (WindowComponents.chosen_question_topic.get() == "Question Topic" or WindowComponents.chosen_question_type == "Question Type"):
            messagebox.showinfo("ERROR", "Question Topic or Type not Selected")
            return None
        
        display_question_list: list[BaseQuestion] = WindowControls.get_questions()


        if display_question_list == None:
            messagebox.showerror("ERROR", "Questions can't be found")
            return None
        if len(display_question_list) == 0:
            messagebox.showinfo("No Questions", "There are Currently No Questions that Fit that Criteria")
            return None

        WindowComponents.question_list.delete(0, END)
        WindowComponents.question_keys.clear()

        for question in display_question_list:
            WindowComponents.question_list.insert('end', question.question_id)
            WindowComponents.question_keys.append(question.question_id)
   
    def get_questions() -> list[BaseQuestion]:
        question_list: list[BaseQuestion] = []

        chosen_usability: str = WindowComponents.chosen_question_usability.get()
        chosen_type: str = WindowComponents.chosen_question_type.get()
        chosen_topic: str = WindowComponents.chosen_question_topic.get()#.split("-")[0].strip();# print(chosen_topic)
        chosen_image: str = WindowComponents.chosen_image_question.get()
        chosen_difficulty: str = WindowComponents.chosen_question_difficulty.get()
        
        if WindowComponents.display_all or (chosen_type == "All" and chosen_topic == "All" and chosen_image == "All" and chosen_difficulty == "All"): return CommonData.usable_questions.copy() + CommonData.discarded_questions.copy()

        # if chosen_usability not in WindowComponents.question_usabilities: return None
        # if chosen_type not in WindowComponents.question_types: return None
        # if chosen_topic not in WindowComponents.question_topics: return None
        # if chosen_image not in WindowComponents.image_question_types: return None
        # if chosen_difficulty not in WindowComponents.question_difficulties: return None

        chosen_topic = chosen_topic.split("-")[0].strip()#; print(chosen_topic)

        match chosen_usability:
            case "Usable": question_list = CommonData.usable_questions.copy()
            case "Discarded": question_list = CommonData.discarded_questions.copy()
            case "All":
                question_list = CommonData.usable_questions.copy() + CommonData.discarded_questions.copy()
                sort_questions(question_list)
        
        question_index: int = 0
        check_question: BaseQuestion = None
        
        keep_images: bool = False

        if chosen_image != "All":
            if chosen_image == "Image Question": keep_images = True
            else: keep_images = False

            while question_index < len(question_list):
                check_question = question_list[question_index]
                if check_question.is_image_question != keep_images: question_list.remove(check_question)
                else: question_index += 1

        question_index = 0
        check_question = None
        
        if chosen_type != "All":
            while question_index < len(question_list):
                check_question = question_list[question_index]
                if check_question.question_type != chosen_type: question_list.remove(check_question)
                else: question_index += 1

        question_index = 0
        check_question = None
        
        if chosen_difficulty != "All":
            while question_index < len(question_list):
                check_question = question_list[question_index]
                if check_question.question_difficulty != chosen_difficulty: question_list.remove(check_question)
                else: question_index += 1

        question_index = 0
        check_question = None
        
        if chosen_topic != "All":
            while question_index < len(question_list):
                check_question = question_list[question_index]
                if chosen_topic not in check_question.question_topics: question_list.remove(check_question)
                else: question_index += 1

        return question_list

    def display_found_questions(question_list: list[BaseQuestion]) -> None:
        questions: list[str] = []
        for question in question_list:
            questions.append(question.question_id)

        # print(questions)

    def display_all_questions() -> None:
        WindowComponents.display_all = True
        WindowControls.display_questions()
        WindowComponents.display_all = False

    def toggle_discarded() -> None:
        WindowComponents.display_discarded = not WindowComponents.display_discarded
        WindowComponents.toggle_question_status.configure(text = f"Toggle Usable: {not WindowComponents.display_discarded}")
        
    def toggle_image() -> None:
        WindowComponents.display_image_questions = not WindowComponents.display_image_questions
        WindowComponents.toggle_image_status.configure(text = f"Display Image: {WindowComponents.display_image_questions}")
        WindowControls.display_questions()

    def clear_question_list() -> None: WindowComponents.question_list.delete(0, END)

    def get_topic_name_list() -> list[str]:
        WindowComponents.question_topics = []

        for topic in CommonData.topic_list:
            WindowComponents.question_topics.append(f"{topic.topic_id} - {topic.topic_name}")
        
        # print(WindowComponents.question_topics)
        
        return WindowComponents.question_topics

    def update_discard_button(event: Event) -> None:
        sort_questions(CommonData.usable_questions)
        # print(WindowComponents.question_list.curselection()[0])
        # print(WindowComponents.question_keys[WindowComponents.question_list.curselection()[0]])
        working_question: BaseQuestion = CommonData.get_usable_question(WindowComponents.question_keys[WindowComponents.question_list.curselection()[0]], 0, len(CommonData.usable_questions))

        if working_question.discarded: WindowComponents.discard_question_button.configure(command = WindowControls.reinstate_question)
        else: WindowComponents.discard_question_button.configure(command = WindowControls.discard_question)

    def discard_question() -> None:
        sort_questions(CommonData.usable_questions)
        working_question: BaseQuestion = CommonData.get_usable_question(WindowComponents.question_list.curselection()[0])

        working_question.discarded = True

        CommonData.usable_questions.remove(working_question)
        CommonData.discarded_questions.append(working_question)

        WindowControls.display_questions()

    def reinstate_question() -> None:
        sort_questions(CommonData.discarded_questions)
        working_question: BaseQuestion = CommonData.get_discarded_question(WindowComponents.question_list.curselection()[0])

        working_question.discarded = False

        CommonData.discarded_questions.remove(working_question)
        CommonData.usable_questions.append(working_question)

        WindowControls.display_questions()

    def toggle_text_hint() -> None:
        WindowComponents.add_text_hint = not WindowComponents.add_text_hint

        WindowComponents.text_hint_button.configure(text = f"Add Text Hint: {WindowComponents.add_text_hint}")

        if WindowComponents.add_text_hint: WindowComponents.text_hint_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        else: WindowComponents.text_hint_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

    def toggle_provide_word_hint() -> None:
        WindowComponents.add_provide_word_hint = not WindowComponents.add_provide_word_hint

        WindowComponents.relevant_hint_button.configure(text = f"Add Provide Word Hint: {WindowComponents.add_provide_word_hint}")

        if WindowComponents.add_provide_word_hint: WindowComponents.relevant_hint_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: WindowComponents.relevant_hint_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

    def toggle_50_50_hint() -> None:
        WindowComponents.add_50_50_hint = not WindowComponents.add_50_50_hint

        WindowComponents.relevant_hint_button.configure(text = f"Add 50/50 Hint: {WindowComponents.add_50_50_hint}")

        if WindowComponents.add_50_50_hint: WindowComponents.relevant_hint_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: WindowComponents.relevant_hint_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

    def toggle_place_one_hint() -> None:
        WindowComponents.add_place_one_hint = not WindowComponents.add_place_one_hint

        WindowComponents.relevant_hint_button.configure(text = f"Add Place One Hint: {WindowComponents.add_50_50_hint}")

        if WindowComponents.add_place_one_hint: WindowComponents.relevant_hint_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: WindowComponents.relevant_hint_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

    def toggle_image_question() -> None:
        WindowComponents.is_image_question = False # not WindowComponents.is_image_question

        WindowComponents.image_question_button.configure(text = f"Image Question: {WindowComponents.is_image_question}")

        if WindowComponents.is_image_question: WindowComponents.image_question_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: WindowComponents.image_question_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)


    # Question Creator Functions
    
    def insert_common_preview_items(preview: dict, y_start: int = 75) -> None:
        WindowComponents.question_difficulty_output.configure(text = f"Question Difficulty: {preview["Question Difficulty"]}")
        WindowComponents.question_score_output.configure(text = f"Question Score: {preview["Question Points"]}")
        WindowComponents.question_text_output.configure(text = f"Question:\n{preview["Question Text"]}")
        WindowComponents.text_hint_output.configure(text = f"Hint Text: {preview["Hints"]["Text Hint"]}")

        # Insert Topics into Shroud
        topic_label: Label
        topic_data: Topic

        for i in range(len(preview["Question Topics"])):
            topic_data = CommonData.get_topic_from_id(preview["Question Topics"][i], 0, len(CommonData.topic_list))

            topic_label = Label(WindowComponents.question_view, text = topic_data.topic_name, bg = CommonData.get_colour_from_id(topic_data.topic_colours[0], 0, len(CommonData.colour_list)).colour_code, fg = CommonData.get_colour_from_id(topic_data.topic_colours[1], 0, len(CommonData.colour_list)).colour_code, font = WindowComponents.main_font)
            topic_label.place(x = 485, y = y_start + (35 * i), width = 175, height = 30)

        WindowComponents.fun_fact_preview = Label(WindowComponents.question_view, text = f"Fun Fact (PREVIEW ONLY): {preview["Fun Fact"]}", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.fun_fact_preview.place(x = 25, y = 400, width = 645, height = 30)

    def view_closed_preview(preview: dict) -> None:
        frame_width: int = 695
        frame_height: int = 450

        WindowComponents.question_view.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.position_frame(WindowComponents.question_view, [frame_width, frame_height])

        WindowControls.insert_common_preview_items(preview)

        # Insert Answers
        answer_count: int = len(preview["Answers"])

        if answer_count < 4: WindowComponents.closed_answers[3].destroy()
        if answer_count < 3: WindowComponents.closed_answers[2].destroy()

        if answer_count == 2:
            WindowComponents.closed_answers[0].place(width = 435) # if not preview["Images"]["Is Image Question"] else 745)
            WindowComponents.closed_answers[1].place(x = 25, y = 245, width = 435) # if not preview["Images"]["Is Image Question"] else 555, width = 435)
        elif answer_count == 3:
            WindowComponents.closed_answers[2].place(width = 435) # if not preview["Images"]["Is Image Question"] else 745)

        for i in range(answer_count):
            WindowComponents.closed_answers[i].configure(text = preview["Answers"][i]["Answer Text"],
                bg = CommonData.get_colour_from_id(preview["Answers"][i]["Answer Back Colour"], 0, len(CommonData.colour_list)).colour_code,
                fg = CommonData.get_colour_from_id(preview["Answers"][i]["Answer Text Colour"], 0, len(CommonData.colour_list)).colour_code)

    def view_open_preview(preview: dict) -> None:
        frame_width: int = 695
        frame_height: int = 425

        WindowComponents.question_view.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.position_frame(WindowComponents.question_view, [frame_width, frame_height])

        WindowControls.insert_common_preview_items(preview, 80)

        WindowComponents.fun_fact_preview.place(y = 370)

    def clear_edit_questions_page(question_type: str) -> None:
        WindowComponents.question_text_input.delete("1.0", END)
        WindowComponents.text_hint_entry.delete("1.0", END)
        WindowComponents.image_file_entry.delete(0, len(WindowComponents.image_file_entry.get()))
        WindowComponents.fun_fact_entry.delete(0, len(WindowComponents.fun_fact_entry.get()))

        # Reset Toggles
        WindowComponents.add_text_hint = True
        WindowComponents.text_hint_button.configure(text = f"Add Text Hint: {WindowComponents.add_text_hint}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

        WindowComponents.is_image_question = False
        WindowComponents.image_question_button.configure(text = f"Image Question: {WindowComponents.is_image_question}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

        # Reset Topics
        WindowComponents.topic_selector.selection_clear(0, END)

        # Reset Difficulty, Score + Audios
        WindowComponents.chosen_difficulty.set("Question Difficulty")
        WindowComponents.chosen_question_score.set("Question Score")
        WindowComponents.chosen_correct_audio.set("Correct Audio")
        WindowComponents.chosen_incorrect_audio.set("Incorrect Audio")

        # Individual Functions for each Question Type
        match question_type:
            case "Closed":
                for answer in WindowComponents.answers: answer.clear()
                WindowComponents.add_50_50_hint = False
                WindowComponents.relevant_hint_button.configure(text = f"Add 50/50 Hint: {WindowComponents.add_50_50_hint}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
            case "Open":
                WindowComponents.add_provide_word_hint = False
                # WindowComponents.relevant_hint_button.configure(text = f"Add Provide Word Hint: {WindowComponents.add_provide_word_hint}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
            case "Order":
                WindowComponents.add_place_one_hint = False
                # WindowComponents.relevant_hint_button.configure(text = f"Add Place One Hint: {WindowComponents.add_place_one_hint}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

    def view_image_preview() -> None: # Needs beautifying (I think thats done now)
        if not QuestionController.valid_image_file():
            messagebox.showerror("Invalid Image File", "The provided Image File is Invalid")
            return False

        image: PIL.Image = PIL.Image.open(WindowComponents.image_file_entry.get().strip(), "r")
        width, height = image.size

        if height > 300:
            width = int(300 * (width / height))
            height = 300

        loaded_image = PIL.ImageTk.PhotoImage(image.resize((width, height)))

        if WindowComponents.image_preview_frame != None and WindowComponents.image_preview_frame.winfo_exists(): WindowComponents.image_preview_frame.destroy()

        WindowComponents.image_preview_frame = Toplevel(WindowComponents.window)
        WindowComponents.image_preview_frame.config(bg = WindowComponents.window_colours[0].colour_code)
        display: Label = Label(WindowComponents.image_preview_frame, image = loaded_image, bg = WindowComponents.window_colours[0].colour_code)
        display.place(x = 10, y = 10); display.img = loaded_image

        WindowComponents.image_preview_frame.geometry(f"{width + 20}x{height + 60}")

        close: Button = Button(WindowComponents.image_preview_frame, text = "Close", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowComponents.image_preview_frame.destroy)
        close.place(x = 10, y = 20 + height, width = 85, height = 30)


    # Insert Question to Frame
    def insert_closed_question_info(question_data: ClosedQuestion, question_number: int) -> None: pass
    def insert_open_question_info(question_data: OpenQuestion, question_number: int) -> None: pass
    def insert_order_question_info(question_data: OrderQuestion, question_number: int) -> None: pass


    # Quiz Setup Functions

    def update_quiz_topics(event: Event) -> None:
        WindowComponents.included_topics.clear()

        id_sort_topics(CommonData.topic_list)
        for topic in WindowComponents.topic_selection.curselection():
            WindowComponents.included_topics.append(CommonData.topic_list[topic].topic_id)

        WindowControls.update_available_questions()

    def toggle_question_type(question_type: str) -> None:
        match question_type:
            case "Closed":
                WindowComponents.include_closed_questions = not WindowComponents.include_closed_questions
                WindowComponents.include_closed_questions_button.configure(text = f"Add Closed Questions: {WindowComponents.include_closed_questions}")

                if WindowComponents.include_closed_questions: WindowComponents.include_closed_questions_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
                else: WindowComponents.include_closed_questions_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
            case "Open":
                WindowComponents.include_open_questions = not WindowComponents.include_open_questions
                WindowComponents.include_open_questions_button.configure(text = f"Add Open Questions: {WindowComponents.include_open_questions}")

                if WindowComponents.include_open_questions: WindowComponents.include_open_questions_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
                else: WindowComponents.include_open_questions_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
            case "Order":
                WindowComponents.include_order_questions = not WindowComponents.include_order_questions
                WindowComponents.include_order_questions_button.configure(text = f"Add Order Questions: {WindowComponents.include_order_questions}")

                if WindowComponents.include_order_questions: WindowComponents.include_order_questions_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
                else: WindowComponents.include_order_questions_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

        WindowControls.update_available_questions()

    def toggle_question_difficulty(question_difficulty: str) -> None:
        match question_difficulty:
            case "Easy":
                WindowComponents.include_easy_questions = not WindowComponents.include_easy_questions
                WindowComponents.include_easy_questions_button.configure(text = f"Add Easy Questions: {WindowComponents.include_easy_questions}")

                if WindowComponents.include_easy_questions: WindowComponents.include_easy_questions_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
                else: WindowComponents.include_easy_questions_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
            case "Medium":
                WindowComponents.include_medium_questions = not WindowComponents.include_medium_questions
                WindowComponents.include_medium_questions_button.configure(text = f"Add Medium Questions: {WindowComponents.include_medium_questions}")

                if WindowComponents.include_medium_questions: WindowComponents.include_medium_questions_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
                else: WindowComponents.include_medium_questions_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
            case "Hard":
                WindowComponents.include_hard_questions = not WindowComponents.include_hard_questions
                WindowComponents.include_hard_questions_button.configure(text = f"Add Hard Questions: {WindowComponents.include_hard_questions}")

                if WindowComponents.include_hard_questions: WindowComponents.include_hard_questions_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
                else: WindowComponents.include_hard_questions_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

        WindowControls.update_available_questions()

    def toggle_include_images() -> None:
        WindowComponents.include_image_questions = not WindowComponents.include_image_questions
        WindowComponents.include_image_questions_button.configure(text = f"Include Image Questions: {WindowComponents.include_image_questions}")

        if WindowComponents.include_image_questions: WindowComponents.include_image_questions_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        else: WindowComponents.include_image_questions_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

        WindowControls.update_available_questions()
    
    def clear_quiz_settings() -> None:
        WindowComponents.include_closed_questions = True
        WindowComponents.include_open_questions = True
        WindowComponents.include_order_questions = False
        
        WindowComponents.include_closed_questions_button.configure(text = f"Add Closed Questions: {WindowComponents.include_closed_questions}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        WindowComponents.include_open_questions_button.configure(text = f"Add Open Questions: {WindowComponents.include_open_questions}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        WindowComponents.include_order_questions_button.configure(text = f"Add Order Questions: {WindowComponents.include_order_questions}", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

        WindowComponents.include_easy_questions = True
        WindowComponents.include_medium_questions = True
        WindowComponents.include_hard_questions = True

        WindowComponents.include_easy_questions_button.configure(text = f"Add Easy Questions: {WindowComponents.include_easy_questions}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        WindowComponents.include_medium_questions_button.configure(text = f"Add Medium Questions: {WindowComponents.include_medium_questions}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        WindowComponents.include_hard_questions_button.configure(text = f"Add Hard Questions: {WindowComponents.include_hard_questions}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

        WindowComponents.include_image_questions = False

        WindowComponents.include_image_questions_button.configure(text = f"Include Image Questions: {WindowComponents.include_image_questions}", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

        WindowComponents.quiz_length_set.configure(from_ = -1, to = 1)
        WindowComponents.quiz_length_set.set(0)

    def update_available_questions() -> None:
        WindowComponents.available_questions = CommonData.usable_questions.copy()

        i: int = 0
        question: BaseQuestion

        while i < len(WindowComponents.available_questions):
            question = WindowComponents.available_questions[i]
            
            if WindowComponents.include_image_questions ^ question.is_image_question == 1:
                WindowComponents.available_questions.remove(question)
                i -= 1
            elif not question.included_topics(WindowComponents.included_topics):
                WindowComponents.available_questions.remove(question)
                i -= 1
            elif not question.correct_difficulty(WindowComponents.include_easy_questions, WindowComponents.include_medium_questions, WindowComponents.include_hard_questions):
                WindowComponents.available_questions.remove(question)
                i -= 1
            elif not question.correct_type(WindowComponents.include_closed_questions, WindowComponents.include_open_questions, WindowComponents.include_order_questions):
                WindowComponents.available_questions.remove(question)
                i -= 1
            
            i += 1

        print()
        for question in WindowComponents.available_questions:
            print(f"{question.question_id} - {question.question_difficulty} / {question.question_type} / {question.is_image_question}")
        
        WindowControls.update_quiz_length_setter()

    def update_quiz_length_setter(do_check: bool = True) -> None:
        # if do_check and len(WindowComponents.available_questions) <= 3:
        #     messagebox.showerror("Insufficient Questions", "Current Settings makes your Quiz too Short")

        total_questions: int = len(WindowComponents.available_questions)
        min_length: int = 1

        if total_questions == 0: min_length = 0

        WindowComponents.quiz_length_set.configure(from_ = min_length, to = total_questions)
        WindowComponents.quiz_length_set.set(min_length)

    def setup_quiz() -> None: pass


    # Quiz Functions

    def submit_answer() -> None: pass
    def next_question() -> None: pass
    def review_question() -> None: pass

    def use_50_50_hint() -> None: pass
    def use_provide_word_hint() -> None: pass
    def use_place_one_hint() -> None: pass

    # Clear Functions

    def clear_colour_selector() -> None: pass

    def clear_edit_accounts_page() -> None:
        WindowComponents.update_username_entry.delete(0, len(WindowComponents.update_username_entry.get()))
        WindowComponents.update_password_entry.delete(0, len(WindowComponents.update_password_entry.get()))


    # Position Frame
    
    def make_active(frame: Toplevel) -> None:
        # frame.withdraw()
        frame.update()
        frame.deiconify()

