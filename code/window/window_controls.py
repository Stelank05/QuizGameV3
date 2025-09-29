import functools
# import PIL.Image
# import PIL.ImageTk

from tkinter import *
from tkinter import messagebox

from classes.colour import Colour

from controls.audio_controls import AudioControls
from controls.colour_controls import ColourControls
from controls.generic_controls import *
from controls.player_controls import *
from controls.question_controller import QuestionController
from controls.sort_functions_quiz import *
from controls.sort_functions import *
from controls.topic_controls import TopicControls

from questions.question_base import BaseQuestion
from questions.question_closed import ClosedQuestion
from questions.question_open import OpenQuestion
from questions.question_order import OrderQuestion

from quiz.answer_past import PastAnswer
from quiz.question_closed_past import PastClosedQuestion
from quiz.question_open_past import PastOpenQuestion
from quiz.question_order_past import PastOrderQuestion
from quiz.quiz import Quiz

from window.question_design import QuestionDesign
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

        WindowComponents.window_colour_widgets = []
        WindowComponents.button_colour_widgets = []
        WindowComponents.label_colour_widgets = []
        WindowComponents.entry_colour_widgets = []

        WindowComponents.black = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list))
        WindowComponents.white = CommonData.get_colour_from_name("White", 0, len(CommonData.colour_list))


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
            "Previous Quizzes": [],
            "Leaderboard Settings": {
                "Hide Max Score": False,
                "Hide Score Percentage": True,
                "Hide Incorrect Count": True,
                "Hide Question Percentage": False,
                "Hide Hint Breakdown": False
            }
        }
    
    def make_colour_list() -> dict:
        return {
            "Window Colours" : [WindowComponents.chosen_window_back.colour_id, WindowComponents.chosen_window_text.colour_id],
            "Button Colours" : [WindowComponents.chosen_button_back.colour_id, WindowComponents.chosen_button_text.colour_id],
            "Label Colours" : [WindowComponents.chosen_label_back.colour_id, WindowComponents.chosen_label_text.colour_id],
            "Entry Colours" : [WindowComponents.chosen_entry_back.colour_id, WindowComponents.chosen_entry_text.colour_id],
        }


    # Past Quiz Viewing

    def update_quiz_outputs(event: Event) -> None:
        if len(WindowComponents.quiz_output.curselection()) == 0: return None
        if not WindowComponents.quiz_output: return None

        sort_quizzes_id(CommonData.past_quizzes)
        WindowComponents.current_past_quiz = CommonData.past_quizzes[WindowComponents.quiz_output.curselection()[0]]

        WindowComponents.quiz_id_output.configure(text = WindowComponents.current_past_quiz.quiz_id)
        WindowComponents.quiz_length_output.configure(text = f"{len(WindowComponents.current_past_quiz.questions)} Questions")
        WindowComponents.quiz_score_output.configure(text = WindowComponents.current_past_quiz.score)
        WindowComponents.quiz_max_score_output.configure(text = WindowComponents.current_past_quiz.max_score)
        WindowComponents.quiz_score_percentage_output.configure(text = WindowComponents.current_past_quiz.percentage)
        WindowComponents.quiz_correct_output.configure(text = f"{WindowComponents.current_past_quiz.correct_count} Questions")
        WindowComponents.quiz_incorrect_output.configure(text = f"{WindowComponents.current_past_quiz.incorrect_count} Questions")

        WindowComponents.quiz_hints_general_output.configure(text = f"{WindowComponents.current_past_quiz.total_hints_used} Hints Used")
        WindowComponents.quiz_hints_text_output.configure(text = f"{WindowComponents.current_past_quiz.text_hints_used} Hints Used")
        WindowComponents.quiz_hints_closed_output.configure(text = f"{WindowComponents.current_past_quiz.closed_hints_used} Hints Used")
        WindowComponents.quiz_hints_open_output.configure(text = f"{WindowComponents.current_past_quiz.open_hints_used} Hints Used")
        WindowComponents.quiz_hints_order_output.configure(text = f"{WindowComponents.current_past_quiz.order_hints_used} Hints Used")

    def clear_quiz_outputs() -> None:
        WindowComponents.quiz_id_output.configure(text = "")
        WindowComponents.quiz_length_output.configure(text = "")
        WindowComponents.quiz_score_output.configure(text = "")
        WindowComponents.quiz_max_score_output.configure(text = "")
        WindowComponents.quiz_score_percentage_output.configure(text = "")
        WindowComponents.quiz_correct_output.configure(text = "")
        WindowComponents.quiz_incorrect_output.configure(text = "")

        WindowComponents.quiz_hints_general_output.configure(text = "")
        WindowComponents.quiz_hints_text_output.configure(text = "")
        WindowComponents.quiz_hints_closed_output.configure(text = "")
        WindowComponents.quiz_hints_open_output.configure(text = "")
        WindowComponents.quiz_hints_order_output.configure(text = "")

    def begin_quiz_review() -> None:
        WindowComponents.review_mode = "Past Quiz"

        WindowComponents.view_past_quiz_page.withdraw()
        WindowControls.review_question(WindowComponents.current_past_quiz.questions[0])


    # Question Functions

    def reset_controls() -> None:
        WindowComponents.chosen_question_type.set("Question Type")
        WindowComponents.chosen_question_topic.set("Question Topic")
        WindowComponents.chosen_image_question.set("Is Image Question")
        WindowComponents.chosen_question_difficulty.set("Question Difficulty")
        WindowComponents.chosen_question_usability.set("Question Usability")

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
    
        WindowComponents.display_questions = display_question_list

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
        
        if WindowComponents.display_all or (chosen_usability == "All" and chosen_type == "All" and chosen_topic == "All" and chosen_image == "All" and chosen_difficulty == "All"): return CommonData.usable_questions.copy() + CommonData.discarded_questions.copy()

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

    def clear_question_list() -> None:
        WindowComponents.question_list.delete(0, END)

    def get_topic_name_list() -> list[str]:
        WindowComponents.question_topics = []

        for topic in CommonData.topic_list:
            WindowComponents.question_topics.append(f"{topic.topic_id} - {topic.topic_name}")
        
        return WindowComponents.question_topics

    def update_discard_button(event: Event) -> None:
        if len(WindowComponents.question_list.curselection()) == 0: return None
        if not WindowComponents.question_select_visible: return None
        
        sort_questions(CommonData.usable_questions)
        working_question: BaseQuestion = CommonData.get_question(WindowComponents.question_keys[WindowComponents.question_list.curselection()[0]], [], 0, len(CommonData.usable_questions))

        if working_question.discarded: WindowComponents.discard_question_button.configure(text = "Reinstate Question", command = WindowControls.invert_usability)
        else: WindowComponents.discard_question_button.configure(text = "Discard Question", command = WindowControls.invert_usability)

    def invert_usability() -> None:
        if len(WindowComponents.question_list.curselection()) == 0: return None

        working_question: BaseQuestion = WindowComponents.display_questions[WindowComponents.question_list.curselection()[0]]

        working_question.discarded = not working_question.discarded

        if not working_question.discarded:
            CommonData.discarded_questions.remove(working_question)
            CommonData.usable_questions.append(working_question)
            WindowComponents.discard_question_button.configure(text = "Discard Question", command = WindowControls.invert_usability)
        else:
            CommonData.usable_questions.remove(working_question)
            CommonData.discarded_questions.append(working_question)
            WindowComponents.discard_question_button.configure(text = "Reinstate Question", command = WindowControls.invert_usability)

        question_file: str = os.path.join(CommonData.question_folder, f"{working_question.question_id}.json")
        write_json_file(question_file, working_question.create_dictionary())

        match WindowControls.decide_display_option():
            case "Select": WindowControls.display_questions()
            case "All": WindowControls.display_all_questions()

    def decide_display_option() -> str:
        def_type: bool = WindowComponents.chosen_question_type.get() == "Question Type"
        def_topic: bool = WindowComponents.chosen_question_topic.get() == "Question Topic"
        def_image: bool = WindowComponents.chosen_image_question.get() == "Is Image Question"
        def_difficulty: bool = WindowComponents.chosen_question_difficulty.get() == "Question Difficulty"
        def_usability: bool = WindowComponents.chosen_question_usability.get() == "Question Usability"

        if def_type or def_topic or def_image or def_difficulty or def_usability: return "All"
        return "Select"

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

        WindowComponents.relevant_hint_button.configure(text = f"Add Place One Hint: {WindowComponents.add_place_one_hint}")

        if WindowComponents.add_place_one_hint: WindowComponents.relevant_hint_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: WindowComponents.relevant_hint_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

    def toggle_image_question() -> None:
        WindowComponents.is_image_question = not WindowComponents.is_image_question

        WindowComponents.image_question_button.configure(text = f"Image Question: {WindowComponents.is_image_question}")

        if WindowComponents.is_image_question: WindowComponents.image_question_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: WindowComponents.image_question_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)


    # Question Creator Functions
    
    def insert_common_preview_items(preview: dict, y_start: int = 75, topic_height: int = 30) -> None:
        WindowComponents.question_difficulty_output.configure(text = f"Question Difficulty: {preview["Question Difficulty"]}")
        WindowComponents.question_score_output.configure(text = f"Question Score: {preview["Question Points"]}")
        WindowComponents.question_text_output.configure(text = f"Question:\n{preview["Question Text"]}")
        
        if WindowComponents.add_text_hint: WindowComponents.text_hint_output.configure(text = f"Hint Text: {preview["Hints"]["Text Hint"]}")
        else: WindowComponents.text_hint_output.configure(text = "Text Hint Not Included")

        # Insert Topics into Shroud
        topic_label: Label
        topic_data: Topic

        for i in range(len(preview["Question Topics"])):
            topic_data = CommonData.get_topic_from_id(preview["Question Topics"][i], 0, len(CommonData.topic_list))

            topic_label = Label(WindowComponents.question_view, text = topic_data.topic_name, bg = CommonData.get_colour_from_id(topic_data.topic_colours[0], 0, len(CommonData.colour_list)).colour_code, fg = CommonData.get_colour_from_id(topic_data.topic_colours[1], 0, len(CommonData.colour_list)).colour_code, font = WindowComponents.main_font)
            topic_label.place(x = 485, y = y_start + ((topic_height + 5) * i), width = 175, height = topic_height)

        WindowComponents.fun_fact_preview = Label(WindowComponents.question_view, text = f"Fun Fact (PREVIEW ONLY): {preview["Fun Fact"]}", wraplength = 600, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.fun_fact_preview.place(x = 25, y = 400, width = 645, height = 60)

    def view_closed_preview(preview: dict) -> None:
        frame_width: int = 695
        frame_height: int = 480

        WindowComponents.question_view.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.position_frame(WindowComponents.question_view, [frame_width, frame_height])

        WindowControls.insert_common_preview_items(preview)

        # Insert Answers
        answer_count: int = len(preview["Answers"])

        if answer_count < 4: WindowComponents.closed_answer_buttons[3].destroy()
        if answer_count < 3: WindowComponents.closed_answer_buttons[2].destroy()

        if answer_count == 2:
            WindowComponents.closed_answer_buttons[0].place(width = 435) # if not preview["Images"]["Is Image Question"] else 745)
            WindowComponents.closed_answer_buttons[1].place(x = 25, y = 245, width = 435) # if not preview["Images"]["Is Image Question"] else 555, width = 435)
        elif answer_count == 3:
            WindowComponents.closed_answer_buttons[2].place(width = 435) # if not preview["Images"]["Is Image Question"] else 745)

        for i in range(answer_count):
            WindowComponents.closed_answer_buttons[i].configure(text = preview["Answers"][i]["Answer Text"],
                bg = CommonData.get_colour_from_id(preview["Answers"][i]["Answer Back Colour"], 0, len(CommonData.colour_list)).colour_code,
                fg = CommonData.get_colour_from_id(preview["Answers"][i]["Answer Text Colour"], 0, len(CommonData.colour_list)).colour_code)

    def view_open_preview(preview: dict) -> None:
        frame_width: int = 695
        frame_height: int = 485

        WindowComponents.question_view.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.position_frame(WindowComponents.question_view, [frame_width, frame_height])
        
        WindowControls.insert_common_preview_items(preview, 80)

        WindowComponents.fun_fact_preview.place(y = 400)

    def view_order_preview(preview: dict) -> None:
        frame_width: int = 695
        frame_height: int = 595

        WindowComponents.question_view.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.position_frame(WindowComponents.question_view, [frame_width, frame_height])

        for i in range(len(preview["Answers"])): WindowComponents.order_answer_entries[i][1].configure(text = preview["Answers"][i])

        WindowControls.insert_common_preview_items(preview, 80, 45)

        WindowComponents.fun_fact_preview.place(y = 510)

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
                WindowComponents.relevant_hint_entry.delete(0, len(WindowComponents.relevant_hint_entry.get()))
                WindowComponents.open_answer_required.delete(0, len(WindowComponents.open_answer_required.get()))
                WindowComponents.open_answer_acceptable.delete(0, len(WindowComponents.open_answer_acceptable.get()))

                WindowComponents.add_provide_word_hint = False
                WindowComponents.relevant_hint_button.configure(text = f"Add Provide Word Hint: {WindowComponents.add_provide_word_hint}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
            case "Order":
                for answer in WindowComponents.order_answers: answer.clear()
                
                WindowComponents.relevant_hint_entry.delete(0, len(WindowComponents.relevant_hint_entry.get()))

                WindowComponents.add_place_one_hint = False
                WindowComponents.relevant_hint_button.configure(text = f"Add Place One Hint: {WindowComponents.add_place_one_hint}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

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

                if WindowComponents.include_order_questions: WindowComponents.include_order_questions_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
                else: WindowComponents.include_order_questions_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

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

        WindowComponents.quiz_length_set.configure(from_ = 0, to = 0)
        WindowComponents.quiz_length_set.set(0)

        WindowComponents.topic_selection.delete(0, END)
        id_sort_topics(CommonData.topic_list)
        for topic in CommonData.topic_list: WindowComponents.topic_selection.insert('end', f"{topic.topic_id} - {topic.topic_name}")

    def update_available_questions() -> None:
        WindowComponents.available_questions = CommonData.usable_questions.copy()

        WindowComponents.available_question_codes.clear()
        for code in WindowComponents.available_questions: WindowComponents.available_question_codes.append(code.question_id)

        i: int = 0
        question: BaseQuestion

        while i < len(WindowComponents.available_questions):
            question = WindowComponents.available_questions[i]
            
            if WindowComponents.include_image_questions ^ question.is_image_question == 1:
                WindowComponents.available_questions.remove(question)
                WindowComponents.available_question_codes.remove(question.question_id)
                i -= 1
            elif not question.included_topics(WindowComponents.included_topics):
                WindowComponents.available_questions.remove(question)
                WindowComponents.available_question_codes.remove(question.question_id)
                i -= 1
            elif not question.correct_difficulty(WindowComponents.include_easy_questions, WindowComponents.include_medium_questions, WindowComponents.include_hard_questions):
                WindowComponents.available_questions.remove(question)
                WindowComponents.available_question_codes.remove(question.question_id)
                i -= 1
            elif not question.correct_type(WindowComponents.include_closed_questions, WindowComponents.include_open_questions, WindowComponents.include_order_questions):
                WindowComponents.available_questions.remove(question)
                WindowComponents.available_question_codes.remove(question.question_id)
                i -= 1
            
            i += 1

        # print()
        # for question in WindowComponents.available_questions:
        #     print(f"{question.question_id} - {question.question_difficulty} / {question.question_type} / {question.is_image_question}")
        
        WindowControls.update_quiz_length_setter()

    def update_quiz_length_setter(do_check: bool = True) -> None:
        total_questions: int = len(WindowComponents.available_questions)
        min_length: int = 1

        if total_questions == 0: min_length = 0
        if total_questions > WindowComponents.max_quiz_length: total_questions = WindowComponents.max_quiz_length

        WindowComponents.quiz_length_set.configure(from_ = min_length, to = total_questions)
        WindowComponents.quiz_length_set.set(min_length)

    def setup_quiz() -> None:
        if WindowComponents.quiz_length_set.get() < WindowComponents.min_quiz_length:
            messagebox.showerror("Insufficient Questions", f"Your Quiz must contain at least {WindowComponents.min_quiz_length} Questions")
            return 0
        
        WindowComponents.review_mode = "Quiz"

        WindowComponents.current_quiz = Quiz()
        WindowComponents.current_quiz.select_questions(WindowComponents.available_question_codes.copy(), int(WindowComponents.quiz_length.get()))

        # Display First Question
        WindowComponents.quiz_setup_page.withdraw()
        WindowControls.next_question(WindowComponents.current_quiz.questions[0])


    # Insert Question to Frame

    def insert_common_quiz_items(question: BaseQuestion, y_start: int = 75, topic_height: int = 30) -> None:
        if WindowComponents.review_mode == "Quiz":
            WindowComponents.question_number_output.configure(text = f"Question Number: {question.question_number} / {len(WindowComponents.current_quiz.questions)}")
            WindowComponents.current_score_output.configure(text = f"Score: {WindowComponents.current_quiz.current_score} / {WindowComponents.current_quiz.theoretical_max}")
        else:
            WindowComponents.question_number_output.configure(text = f"Question Number: {question.question_number} / {len(WindowComponents.current_past_quiz.questions)}")
            WindowComponents.current_score_output.configure(text = f"Score: {WindowComponents.current_past_quiz.score} / {WindowComponents.current_past_quiz.max_score}")

        WindowComponents.question_difficulty_output.configure(text = f"Question Difficulty: {question.question_difficulty}")
        WindowComponents.question_score_output.configure(text = f"Points Available: {question.question_points}")
        WindowComponents.question_text_output.configure(text = f"Question:\n{question.question_text}")

        WindowComponents.exit_quiz_button.configure(command = WindowControls.exit_quiz)

        if question.add_text_hint: WindowComponents.view_text_hint_button.configure(command = functools.partial(WindowControls.use_text_hint, question))
        else: WindowComponents.view_text_hint_button.configure(text = "View Text Hint (UNAVAILABLE)")

        WindowComponents.submit_answer.configure(command = functools.partial(WindowControls.submit_answer, question))

        WindowComponents.review_next_question.configure(text = "Review Next Question")

        if WindowComponents.review_mode == "Quiz":
            if question.question_number > 1: WindowComponents.review_last_question.configure(command = functools.partial(WindowControls.review_question, WindowComponents.current_quiz.questions[question.question_number - 2]))
            if question.question_number < WindowComponents.current_quiz.question_number: WindowComponents.review_next_question.configure(command = functools.partial(WindowControls.review_question, WindowComponents.current_quiz.questions[question.question_number]))

        # Insert Topics into Shroud
        topic_label: Label
        topic_data: Topic

        for i in range(len(question.question_topics)):
            topic_data = CommonData.get_topic_from_id(question.question_topics[i], 0, len(CommonData.topic_list))

            topic_label = Label(WindowComponents.question_view, text = topic_data.topic_name, bg = CommonData.get_colour_from_id(topic_data.topic_colours[0], 0, len(CommonData.colour_list)).colour_code, fg = CommonData.get_colour_from_id(topic_data.topic_colours[1], 0, len(CommonData.colour_list)).colour_code, font = WindowComponents.main_font)
            topic_label.place(x = 485, y = y_start + ((topic_height + 5) * i), width = 175, height = topic_height)

    def insert_closed_question_info(question_data: PastClosedQuestion) -> None:
        question_data.awarded_points = question_data.question_points
        WindowControls.insert_common_quiz_items(question_data) #, review)

        if question_data.add_50_50_hint: WindowComponents.view_relevant_hint_button.configure(command = functools.partial(WindowControls.use_50_50_hint, question_data))
        else: WindowComponents.view_relevant_hint_button.configure(text = "Use 50/50 Hint (UNAVAILABLE)")

        WindowComponents.quiz_answers = question_data.answers.copy()
        WindowControls.sort_answers()

        # Insert Answers
        answer_count: int = len(WindowComponents.quiz_answers)

        if answer_count < 4: WindowComponents.closed_answer_buttons[3].destroy()
        if answer_count < 3: WindowComponents.closed_answer_buttons[2].destroy()

        if answer_count == 2:
            WindowComponents.closed_answer_buttons[0].place(width = 435) # if not preview["Images"]["Is Image Question"] else 745)
            WindowComponents.closed_answer_buttons[1].place(x = 25, y = 245, width = 435) # if not preview["Images"]["Is Image Question"] else 555, width = 435)
        elif answer_count == 3:
            WindowComponents.closed_answer_buttons[2].place(width = 435) # if not preview["Images"]["Is Image Question"] else 745)

        answer_button: Button

        for answer in WindowComponents.quiz_answers:
            answer_button = WindowComponents.closed_answer_buttons[answer.display_index]

            answer_button.configure(text = answer.answer_text,
                bg = CommonData.get_colour_from_id(answer.answer_back_colour, 0, len(CommonData.colour_list)).colour_code,
                fg = CommonData.get_colour_from_id(answer.answer_text_colour, 0, len(CommonData.colour_list)).colour_code,
                command = functools.partial(WindowControls.select_answer, answer_button, answer))
            
            if answer.correct_answer: WindowComponents.correct_answer_button = answer_button
        
    def insert_open_question_info(question_data: PastOpenQuestion) -> None:
        question_data.awarded_points = question_data.question_points
        WindowControls.insert_common_quiz_items(question_data)

        if question_data.provide_word_hint: WindowComponents.view_relevant_hint_button.configure(command = functools.partial(WindowControls.use_provide_word_hint, question_data))
        else: WindowComponents.view_relevant_hint_button.configure(text = "Provide Word Hint (UNAVAILABLE)")

    def insert_order_question_info(question_data: PastOrderQuestion) -> None:
        question_data.awarded_points = question_data.question_points
        WindowControls.insert_common_quiz_items(question_data, 80, 40)

        answer_index: int = 0
        for i in range(len(question_data.displayed_order)):
            WindowComponents.order_answer_entries[i][1].configure(text = question_data.displayed_order[i])
            answer_index += 1
        
        while answer_index < 12:
            WindowComponents.order_answer_entries[answer_index][0].configure(state = 'disabled', disabledbackground = WindowComponents.entry_colours[1].colour_code) #, disabledforeground = WindowComponents.entry_colours[0].colour_code)
            answer_index += 1

        if question_data.place_one_hint: WindowComponents.view_relevant_hint_button.configure(command = functools.partial(WindowControls.use_place_one_hint, question_data))
        else: WindowComponents.view_relevant_hint_button.configure(text = "Place One Hint (UNAVAILABLE)")


    # Set Review Details

    def insert_common_review_items(question_data: BaseQuestion) -> None:
        WindowControls.insert_common_quiz_items(question_data)

        if question_data.text_hint_used: WindowComponents.text_hint_output.configure(text = f"Hint Text: {question_data.text_hint}")


        if WindowComponents.review_mode == "Quiz":
            next_question: BaseQuestion = WindowComponents.current_quiz.questions[WindowComponents.current_quiz.question_number - 1]
            if not WindowComponents.current_quiz.quiz_complete: WindowControls.quiz_review_controls(question_data, next_question)
            else: WindowControls.post_quiz_review_controls(question_data)
        else:
            WindowControls.past_quiz_review_controls(question_data)

    def quiz_review_controls(question_data: BaseQuestion, next_question: BaseQuestion) -> None:
        if question_data.question_number == WindowComponents.current_quiz.question_number - 1: WindowComponents.review_next_question.configure(command = functools.partial(WindowControls.next_question, next_question))
        else: WindowComponents.review_next_question.configure(command = functools.partial(WindowControls.review_question, WindowComponents.current_quiz.questions[question_data.question_number]))

        if question_data.question_number > 1: WindowComponents.review_last_question.configure(command = functools.partial(WindowControls.review_question, WindowComponents.current_quiz.questions[question_data.question_number - 2]))

        WindowComponents.submit_answer.configure(text = "Return to Current Question", command = functools.partial(WindowControls.next_question, next_question))
        
    def post_quiz_review_controls(question_data: BaseQuestion) -> None:
        if question_data.question_number == WindowComponents.current_quiz.question_number: WindowComponents.review_next_question.configure(command = WindowControls.exit_review)
        else: WindowComponents.review_next_question.configure(command = functools.partial(WindowControls.review_question, WindowComponents.current_quiz.questions[question_data.question_number]))

        if question_data.question_number > 1: WindowComponents.review_last_question.configure(command = functools.partial(WindowControls.review_question, WindowComponents.current_quiz.questions[question_data.question_number - 2]))

        WindowComponents.submit_answer.configure(text = "Exit Quiz Review", command = WindowControls.exit_review)
        WindowComponents.exit_quiz_button.configure(command = WindowControls.exit_review)

    def past_quiz_review_controls(question_data: BaseQuestion) -> None:
        if question_data.question_number == len(WindowComponents.current_past_quiz.questions): WindowComponents.review_next_question.configure(command = WindowControls.exit_review)
        else: WindowComponents.review_next_question.configure(command = functools.partial(WindowControls.review_question, WindowComponents.current_past_quiz.questions[question_data.question_number]))

        if question_data.question_number > 1: WindowComponents.review_last_question.configure(command = functools.partial(WindowControls.review_question, WindowComponents.current_past_quiz.questions[question_data.question_number - 2]))

        WindowComponents.submit_answer.configure(text = "Exit Quiz Review", command = WindowControls.exit_review)
        WindowComponents.exit_quiz_button.configure(command = WindowControls.exit_review)

    def insert_closed_review_info(question_data: PastClosedQuestion) -> None:
        WindowControls.insert_common_review_items(question_data)

        if question_data.add_50_50_hint: WindowComponents.view_relevant_hint_button.configure(command = functools.partial(WindowControls.use_50_50_hint, question_data))
        else: WindowComponents.view_relevant_hint_button.configure(text = "Use 50/50 Hint (UNAVAILABLE)")

        WindowComponents.quiz_answers = question_data.answers.copy()
        WindowControls.sort_answers()

        # Insert Answers
        answer_count: int = len(WindowComponents.quiz_answers)

        if answer_count < 4: WindowComponents.closed_answer_buttons[3].destroy()
        if answer_count < 3: WindowComponents.closed_answer_buttons[2].destroy()

        if answer_count == 2:
            WindowComponents.closed_answer_buttons[0].place(width = 435) # if not preview["Images"]["Is Image Question"] else 745)
            WindowComponents.closed_answer_buttons[1].place(x = 25, y = 245, width = 435) # if not preview["Images"]["Is Image Question"] else 555, width = 435)
        elif answer_count == 3:
            WindowComponents.closed_answer_buttons [2].place(width = 435) # if not preview["Images"]["Is Image Question"] else 745)

        answer_button: Button

        answer_background: str # = ""
        answer_foreground: str # = ""

        for answer in WindowComponents.quiz_answers:
            answer_button = WindowComponents.closed_answer_buttons[answer.display_index]

            if answer.answer_hidden:
                answer_button.destroy()
                continue

            if answer.answer_chosen and answer.correct_answer:
                answer_background = CommonData.get_colour_from_name("Green", 0, len(CommonData.colour_list)).colour_code
                answer_foreground = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code
            elif answer.answer_chosen and not answer.correct_answer:
                answer_background = CommonData.get_colour_from_name("Red", 0, len(CommonData.colour_list)).colour_code
                answer_foreground = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code
            elif answer.correct_answer:
                answer_background = CommonData.get_colour_from_name("Indigo", 0, len(CommonData.colour_list)).colour_code
                answer_foreground = CommonData.get_colour_from_name("White", 0, len(CommonData.colour_list)).colour_code
            else:
                answer_background = CommonData.get_colour_from_id(answer.answer_back_colour, 0, len(CommonData.colour_list)).colour_code
                answer_foreground = CommonData.get_colour_from_id(answer.answer_text_colour, 0, len(CommonData.colour_list)).colour_code

            answer_button.configure(text = answer.answer_text, bg = answer_background, fg = answer_foreground)
            
            if answer.correct_answer: WindowComponents.correct_answer_button = answer_button

    def insert_open_review_info(question_data: PastOpenQuestion) -> None:
        WindowControls.insert_common_review_items(question_data)

        # Insert User Text Answer
        WindowComponents.open_answer_entry.insert("1.0", question_data.entered_answer)

        # Insert Provided Word Hint (If Given)
        if question_data.relevant_hint_used:
            hint_label: Label = Label(WindowComponents.question_view, text = f"Provided Word: {question_data.provided_word}", bg = WindowComponents.entry_colours[1].colour_code, fg = WindowComponents.entry_colours[0].colour_code, font = WindowComponents.main_font)
            hint_label.place(x = 25, y = 230, width = 435, height = 30)

        # Insert In/Correct Answer Box
        results_label_text: str; background_colour: str; foreground_colour: str

        if question_data.answered_correctly:
            results_label_text = "Correct Answer!"
            background_colour = CommonData.get_colour_from_name("Green", 0, len(CommonData.colour_list)).colour_code
            foreground_colour = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code
        else:
            results_label_text = f"Wrong Answer. Correct Answer: {question_data.create_correct_answer_string()}"
            background_colour = CommonData.get_colour_from_name("Red", 0, len(CommonData.colour_list)).colour_code
            foreground_colour = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code

        result_label: Label = Label(WindowComponents.question_view, text = results_label_text, bg = background_colour, fg = foreground_colour, font = WindowComponents.main_font)
        result_label.place(x = 25, y = 260, width = 435, height = 30)

    def insert_order_review_info(question_data: PastOrderQuestion) -> None:
        WindowControls.insert_common_review_items(question_data)

        for i in range(len(question_data.displayed_order)):
            WindowComponents.order_answer_entries[i][0].insert(0, question_data.entered_order[i][0])
            WindowComponents.order_answer_entries[i][1].configure(text = question_data.displayed_order[i])

        for i in range(len(WindowComponents.order_answer_entries)):
            WindowComponents.order_answer_entries[i][0].configure(state = 'disabled', disabledbackground = WindowComponents.entry_colours[1].colour_code)

        WindowControls.set_order_feedback(question_data, question_data.entered_order)


    # Quiz Functions

    def select_answer(answer_button: Button, answer: PastAnswer) -> None:
        if not WindowComponents.permit_answer: return None

        if WindowComponents.selected_answer != None:
            WindowComponents.selected_answer.answer_chosen = False
            WindowComponents.closed_answer_buttons[WindowComponents.selected_answer.display_index].configure(
                bg = CommonData.get_colour_from_id(WindowComponents.quiz_answers[WindowComponents.selected_answer.display_index].answer_back_colour, 0, len(CommonData.colour_list)).colour_code,
                fg = CommonData.get_colour_from_id(WindowComponents.quiz_answers[WindowComponents.selected_answer.display_index].answer_text_colour, 0, len(CommonData.colour_list)).colour_code)

            WindowComponents.selected_answer = None
            WindowComponents.selected_button = None

        answer.answer_chosen = True
        WindowComponents.selected_answer = answer
        WindowComponents.selected_button = answer_button

        answer_button.configure(
            bg = CommonData.get_colour_from_id(answer.answer_text_colour, 0, len(CommonData.colour_list)).colour_code,
            fg = CommonData.get_colour_from_id(answer.answer_back_colour, 0, len(CommonData.colour_list)).colour_code)

    def submit_answer(question: BaseQuestion) -> None:
        if question.question_type == "Closed" and WindowComponents.selected_answer == None: return 0
        if question.question_type == "Open" and WindowComponents.open_answer_entry.get("1.0", END)[:-1] == "": return 0
        if question.question_type == "Order" and not WindowControls.order_answered_entered(question): return 0    

        fun_fact_y_level: int = 330
        correct_answer: bool = False
        WindowComponents.permit_answer = False

        match question.question_type:
            case "Closed":
                if WindowComponents.selected_answer.correct_answer:
                    question.answered_correctly = True
                    WindowComponents.selected_button.configure(
                        bg = CommonData.get_colour_from_name("Green", 0, len(CommonData.colour_list)).colour_code,
                        fg = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code)
                else:
                    WindowComponents.selected_button.configure(
                        bg = CommonData.get_colour_from_name("Red", 0, len(CommonData.colour_list)).colour_code,
                        fg = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code)
                    
                    WindowComponents.correct_answer_button.configure(
                        bg = CommonData.get_colour_from_name("Indigo", 0, len(CommonData.colour_list)).colour_code,
                        fg = CommonData.get_colour_from_name("White", 0, len(CommonData.colour_list)).colour_code)
                    
                WindowComponents.selected_answer = None
                WindowComponents.selected_button = None           
            case "Open":
                question.entered_answer = WindowComponents.open_answer_entry.get("1.0", END)[:-1]
                correct_answer = question.valid_answer(question.entered_answer)

                if question.relevant_hint_used: WindowComponents.open_hint_output.place(y = 230)

                if correct_answer:
                    question.answered_correctly = True
                    result_label: Label = Label(WindowComponents.question_view, text = "Correct Answer!", bg = CommonData.get_colour_from_name("Green", 0, len(CommonData.colour_list)).colour_code, fg = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code, font = WindowComponents.main_font)
                    result_label.place(x = 25, y = 260, width = 435, height = 30)
                else:
                    result_label: Label = Label(WindowComponents.question_view, text = f"Wrong Answer. Correct Answer: {question.create_correct_answer_string()}", bg = CommonData.get_colour_from_name("Red", 0, len(CommonData.colour_list)).colour_code, fg = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code, font = WindowComponents.main_font)
                    result_label.place(x = 25, y = 260, width = 435, height = 30) 
            case "Order":
                for i in range(len(question.correct_order)): WindowComponents.order_answer_entries[i][0].configure(state = 'disabled')

                fun_fact_y_level = 440

                question.entered_order = WindowControls.create_order_input(question)
                question.answered_correctly = question.valid_answer(question.entered_order.copy())
                
                WindowControls.set_order_feedback(question, question.entered_order)

        WindowComponents.current_quiz.theoretical_max += question.question_points

        if question.answered_correctly:
            WindowComponents.current_quiz.current_score += round(question.awarded_points, 1)
            WindowComponents.current_quiz.correct_count += 1
            AudioControls.play_audio(CommonData.get_audio_from_id(question.correct_audio, CommonData.full_audio_list, 0, len(CommonData.full_audio_list)).audio_file)
        else:
            WindowComponents.current_quiz.incorrect_count += 1
            AudioControls.play_audio(CommonData.get_audio_from_id(question.incorrect_audio,CommonData.full_audio_list,  0, len(CommonData.full_audio_list)).audio_file)

        WindowComponents.current_score_output.configure(text = f"Score: {WindowComponents.current_quiz.current_score} / {WindowComponents.current_quiz.theoretical_max}")
        fun_fact_label: Label = Label(WindowComponents.question_view, text = f"Fun Fact: {question.fun_fact}", wraplength = 600, bg = WindowComponents.window_colours[1].colour_code, fg = WindowComponents.window_colours[0].colour_code, font = WindowComponents.main_font)
        fun_fact_label.place(x = 25, y = fun_fact_y_level, width = 645, height = 65)

        if question.question_number < len(WindowComponents.current_quiz.questions): WindowComponents.submit_answer.configure(text = "Next Question", command = WindowControls.next_question)
        else: WindowComponents.submit_answer.configure(text = "Finish Quiz", command = WindowControls.finish_quiz)

    def create_order_input(question: PastOrderQuestion) -> list[tuple[int, str]]:
        return_list: list[tuple[int, str]] = []

        # Go through User Input + Put Inputs to list with Index
        input_index: list[tuple[int, int]] = []
        for i in range(len(question.displayed_order)):
            input_index.append([int(WindowComponents.order_answer_entries[i][0].get().strip()), i])

        # Order List by Input
        WindowControls.reorder_list(input_index, 0)
        
        # Go back through the list, dropping each input to 1-X
        for i in range(len(input_index)): input_index[i][0] = i + 1

        # Reorder the list by Index
        WindowControls.reorder_list(input_index, 1)

        # Put new Order Indexes into new List with Displayed Item
        for i in range(len(question.displayed_order)):
            return_list.append([input_index[i][0], question.displayed_order[i]])

        return return_list
    
    def order_answered_entered(question: PastOrderQuestion) -> bool:
        for i in range(len(question.displayed_order)):
            if WindowComponents.order_answer_entries[i][0].get() == "": return False
        return True

    def reorder_list(input_index: list[tuple[int, int]], index: int) -> list[tuple[int, int]]:
        swap: bool
        temp: tuple[int, int]
        
        for i in range(len(input_index) - 1):
            swap = False

            for j in range(len(input_index) - i - 1):
                if input_index[j][index] > input_index[j + 1][index]:
                    swap = True
            
                    temp = input_index[j]
                    input_index[j] = input_index[j + 1]
                    input_index[j + 1] = temp
            
            if not swap: break

        return input_index

    def set_order_feedback(question: PastOrderQuestion, answer: list[tuple[int, str]]) -> None:
        for i in range(len(question.correct_order)):
            if answer[i][1] == question.correct_order[int(answer[i][0]) - 1]: WindowComponents.order_answer_entries[i][0].configure(disabledbackground = CommonData.get_colour_from_name("Green", 0, len(CommonData.colour_list)).colour_code, disabledforeground = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code)
            else: WindowComponents.order_answer_entries[i][0].configure(disabledbackground = CommonData.get_colour_from_name("Red", 0, len(CommonData.colour_list)).colour_code, disabledforeground = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code)

    def next_question(question: BaseQuestion | None = None) -> None:
        # Display Question
        if question == None:
            question: BaseQuestion = WindowComponents.current_quiz.questions[WindowComponents.current_quiz.question_number]
            WindowComponents.current_quiz.question_number += 1

        WindowComponents.permit_answer = True

        if WindowComponents.question_view != None: WindowComponents.question_view.destroy()

        match question.question_type:
            case "Closed":
                QuestionDesign.create_closed_question_view(question.is_image_question)
                WindowControls.insert_closed_question_info(question)
            case "Open":
                QuestionDesign.create_open_question_view(question.is_image_question)
                WindowControls.insert_open_question_info(question)
            case "Order":
                QuestionDesign.create_order_question_view(question.is_image_question)
                WindowControls.insert_order_question_info(question)

    def review_question(question: BaseQuestion) -> None:
        if WindowComponents.question_view != None: WindowComponents.question_view.destroy()

        match question.question_type:
            case "Closed":
                QuestionDesign.create_closed_question_view(question.is_image_question)
                WindowControls.insert_closed_review_info(question)
            case "Open":
                QuestionDesign.create_open_question_view(question.is_image_question)
                WindowControls.insert_open_review_info(question)
            case "Order":
                QuestionDesign.create_order_question_view(question.is_image_question)
                WindowControls.insert_order_review_info(question)

    def begin_review() -> None:
        view_question: BaseQuestion

        if WindowComponents.review_mode == "Quiz":
            WindowComponents.finish_quiz_page.withdraw()
            view_question = WindowComponents.current_quiz.questions[0]
        else:
            WindowComponents.view_past_quiz_page.withdraw()
            view_question = WindowComponents.current_past_quiz.questions[0]
        
        WindowControls.review_question(view_question)
    
    def exit_review() -> None:
        WindowComponents.question_view.destroy()

        if WindowComponents.review_mode == "Quiz":
            WindowComponents.finish_quiz_page.update()
            WindowComponents.finish_quiz_page.deiconify()
        elif WindowComponents.review_mode == "Past Quiz":
            WindowComponents.view_past_quiz_page.update()
            WindowComponents.view_past_quiz_page.deiconify()
        else:
            WindowComponents.view_leaderboard_page.update()
            WindowComponents.view_leaderboard_page.deiconify()
    
    def finish_quiz() -> None:
        WindowComponents.current_quiz.quiz_complete = True
        # Do Post Quiz Quiz Stuff (Create as Past Quiz, Save Details File, Add to Leaderboard, Add to Past Quizzes)

        WindowComponents.question_view.destroy()
        QuestionDesign.make_finish_quiz_page(WindowComponents.window)
        
        # Insert Page Functions
        WindowComponents.retake_quiz_button.configure(command = WindowControls.retake_quiz) # I will write these Functions another time but for now they aren't entirely necessary
        WindowComponents.review_quiz_button_finish.configure(command = WindowControls.begin_review)
        WindowComponents.exit_quiz_button_finish.configure(command = WindowControls.return_to_setup)

        # Convert Quiz to Past Quiz
        quiz_dict: dict
        
        if type(WindowComponents.active_user) == Player: quiz_dict = WindowComponents.current_quiz.create_dictionary(WindowComponents.active_user.user_id)
        else: quiz_dict = WindowComponents.current_quiz.create_dictionary(WindowComponents.active_user.guest_id)

        past_quiz: PastQuiz = PastQuiz(quiz_dict, question_folder = CommonData.question_folder)
        CommonData.past_quizzes.append(past_quiz)
        write_json_file(os.path.join(CommonData.quizzes_folder, f"{quiz_dict["Quiz ID"]}.json"), quiz_dict)
        
        if type(WindowComponents.active_user) == Player:
            WindowComponents.active_user.previous_attempts.append(past_quiz.quiz_id)
            WindowControls.update_user_high_score()
            write_user_file(WindowComponents.active_user)

    def exit_quiz() -> None:
        WindowComponents.question_view.destroy()

        if WindowComponents.finish_quiz_page != None and WindowComponents.finish_quiz_page.winfo_exists():
            WindowComponents.finish_quiz_page.update()
            WindowComponents.finish_quiz_page.deiconify()
        else:
            WindowComponents.quiz_setup_page.update()
            WindowComponents.quiz_setup_page.deiconify()

    def return_to_setup() -> None:
        # Destroy Finish Page
        WindowComponents.finish_quiz_page.destroy()

        # Open Setup Page (Retain Quiz Setup Data?)
        WindowComponents.quiz_setup_page.update()
        WindowComponents.quiz_setup_page.deiconify()
        
    def retake_quiz() -> None:
        WindowComponents.finish_quiz_page.destroy()
        
        questions: list[BaseQuestion] = []

        question_data: dict

        for i in range(len(WindowComponents.current_quiz.questions)):
            question_data = CommonData.get_question(WindowComponents.current_quiz.questions[i].question_id, []).create_dictionary()

            match question_data["Question Type"]:
                case "Closed": questions.append(PastClosedQuestion(question_data, None, i + 1))
                case "Open": questions.append(PastOpenQuestion(question_data, None, i + 1))
                case "Order": questions.append(PastOrderQuestion(question_data, None, i + 1))

        WindowComponents.current_quiz = Quiz()
        WindowComponents.current_quiz.randomise_questions(questions)

        # Display First Question
        WindowComponents.quiz_setup_page.withdraw()
        WindowControls.next_question(WindowComponents.current_quiz.questions[0])

    def update_user_high_score() -> None:
        quiz_list: list[PastQuiz] = []

        for quiz in WindowComponents.active_user.previous_attempts: quiz_list.append(CommonData.get_past_quiz(quiz, 0, len(CommonData.past_quizzes)))
        
        sort_quizzes_id(quiz_list)
        order_quiz_length_hl(quiz_list)
        order_max_score(quiz_list)
        order_score_percentage(quiz_list)

        WindowComponents.active_user.high_score = quiz_list[0].score
        WindowComponents.active_user.high_score_percentage = quiz_list[0].percentage

    #  Hints

    def use_text_hint(question: BaseQuestion) -> None:
        if question.text_hint_used: return 0

        question.awarded_points = round(question.awarded_points - question.hint_penalty, 2)
        WindowComponents.question_score_output.configure(text = f"Points Available: {question.awarded_points}")

        question.text_hint_used = True
        WindowComponents.current_quiz.text_hints_used += 1

        WindowComponents.text_hint_output.configure(text = f"Hint Text: {question.text_hint}")

    def use_50_50_hint(question: PastClosedQuestion) -> None:
        if question.relevant_hint_used: return 0

        question.awarded_points = round(question.awarded_points - question.hint_penalty, 2)
        WindowComponents.question_score_output.configure(text = f"Points Available: {question.awarded_points}")

        question.relevant_hint_used = True
        WindowComponents.current_quiz.closed_hints_used += 1

        answers: list[PastAnswer] = WindowComponents.quiz_answers.copy()
        buttons: list[Button] = WindowComponents.closed_answer_buttons.copy()

        for i in range(len(answers)):
            if answers[i].correct_answer:
                answers.pop(i); buttons.pop(i)
                break
        
        kept_answer: int = random.randint(0, 2)
        answers.pop(kept_answer); buttons.pop(kept_answer)

        for i in range(len(answers)):
            answers[i].answer_hidden = True
            buttons[i].place_forget()   

    def use_provide_word_hint(question: PastOpenQuestion) -> None:
        if question.relevant_hint_used: return 0

        question.awarded_points = round(question.awarded_points - question.hint_penalty, 2)
        WindowComponents.question_score_output.configure(text = f"Points Available: {question.awarded_points}")

        question.relevant_hint_used = True
        WindowComponents.current_quiz.open_hints_used += 1

        WindowComponents.open_hint_output = Label(WindowComponents.question_view, text = f"Provided Word: {question.provided_word}", bg = WindowComponents.entry_colours[1].colour_code, fg = WindowComponents.entry_colours[0].colour_code, font = WindowComponents.main_font)
        WindowComponents.open_hint_output.place(x = 25, y = 260, width = 435, height = 30)

    def use_place_one_hint(question: PastOrderQuestion) -> None:
        if question.relevant_hint_used: return 0

        question.awarded_points = round(question.awarded_points - question.hint_penalty, 2)
        WindowComponents.question_score_output.configure(text = f"Points Available: {question.awarded_points}")

        question.relevant_hint_used = True
        WindowComponents.current_quiz.order_hints_used += 1

        entry_widget: Entry
        
        for i in range(len(question.displayed_order)):
            if question.displayed_order[i] == question.placed_word:
                entry_widget = WindowComponents.order_answer_entries[i][0]

        entry_widget.delete(0, len(entry_widget.get()))
        entry_widget.insert(0, question.placed_index)
        entry_widget.configure(state = 'disabled', disabledbackground = WindowComponents.entry_colours[1].colour_code, disabledforeground = WindowComponents.entry_colours[0].colour_code)

    def sort_answers() -> None:
        temp: PastAnswer
        swap: bool

        for i in range(len(WindowComponents.quiz_answers) - 1):
            swap = False

            for j in range(len(WindowComponents.quiz_answers) - i - 1):
                if WindowComponents.quiz_answers[j].display_index > WindowComponents.quiz_answers[j + 1].display_index:
                    swap = True
                    temp = WindowComponents.quiz_answers[j]
                    WindowComponents.quiz_answers[j] = WindowComponents.quiz_answers[j + 1]
                    WindowComponents.quiz_answers[j + 1] = temp

            if not swap: break


    # Leaderboard Functions

    def display_quizzes() -> None:
        disp_count: int = len(CommonData.past_quizzes)
        if len(WindowComponents.quiz_rows) < disp_count: disp_count = len(WindowComponents.quiz_rows)

        WindowControls.clear_quizzes()
        for i in range(disp_count):
            WindowComponents.quiz_rows[i].set_quiz(CommonData.past_quizzes[i], WindowComponents.active_user, f"P{i + 1}")
            WindowComponents.quiz_rows[i].review_button.configure(command = functools.partial(WindowControls.begin_past_review, CommonData.past_quizzes[i]))

    def clear_quizzes() -> None:
        for i in range(len(WindowComponents.quiz_rows)): WindowComponents.quiz_rows[i].clear_quiz(WindowComponents.active_user)
    
    def begin_past_review(quiz: PastQuiz) -> None:
        WindowComponents.current_past_quiz = quiz

        WindowComponents.review_mode = "Review Quiz"

        WindowComponents.view_leaderboard_page.withdraw()
        WindowControls.review_question(WindowComponents.current_past_quiz.questions[0])

    def display_all_quizzes() -> None:
        sort_quizzes_id(CommonData.past_quizzes)
        WindowControls.display_quizzes()

    def display_correct() -> None:
        sort_quizzes_id(CommonData.past_quizzes)
        order_quiz_length_lh(CommonData.past_quizzes)
        order_max_score(CommonData.past_quizzes)
        order_correct_percentage(CommonData.past_quizzes)
        order_correct(CommonData.past_quizzes)
        WindowControls.display_quizzes()

    def display_incorrect() -> None:
        sort_quizzes_id(CommonData.past_quizzes)
        order_quiz_length_lh(CommonData.past_quizzes)
        order_max_score(CommonData.past_quizzes)
        order_correct_percentage(CommonData.past_quizzes)
        order_incorrect(CommonData.past_quizzes)
        WindowControls.display_quizzes()

    def display_correct_percentage() -> None:
        sort_quizzes_id(CommonData.past_quizzes)
        order_quiz_length_hl(CommonData.past_quizzes)
        order_max_score(CommonData.past_quizzes)
        order_correct_percentage(CommonData.past_quizzes)
        WindowControls.display_quizzes()

    def display_score() -> None:
        sort_quizzes_id(CommonData.past_quizzes)
        order_quiz_length_lh(CommonData.past_quizzes)
        order_score_percentage(CommonData.past_quizzes)
        order_score(CommonData.past_quizzes)
        WindowControls.display_quizzes()

    def display_max_score() -> None:
        sort_quizzes_id(CommonData.past_quizzes)
        order_quiz_length_lh(CommonData.past_quizzes)
        order_max_score(CommonData.past_quizzes)
        WindowControls.display_quizzes()

    def display_score_percentage() -> None:
        sort_quizzes_id(CommonData.past_quizzes)
        order_quiz_length_hl(CommonData.past_quizzes)
        order_max_score(CommonData.past_quizzes)
        order_score_percentage(CommonData.past_quizzes)
        WindowControls.display_quizzes()

    def display_hints_used() -> None:
        sort_quizzes_id(CommonData.past_quizzes)
        order_max_score(CommonData.past_quizzes)
        order_score_percentage(CommonData.past_quizzes)
        order_quiz_length_hl(CommonData.past_quizzes)
        order_hints_used(CommonData.past_quizzes)
        WindowControls.display_quizzes()


    # Leaderboard Settings Functions

    def set_leaderboard_settings() -> None:
        WindowComponents.max_score = "Hidden" if WindowComponents.active_user.hide_max_score else "Visible"
        WindowComponents.score_percentage = "Hidden" if WindowComponents.active_user.hide_score_percentage else "Visible"
        WindowComponents.incorrect_count = "Hidden" if WindowComponents.active_user.hide_incorrect_count else "Visible"
        WindowComponents.question_percentage = "Hidden" if WindowComponents.active_user.hide_questions_percentage else "Visible"
        WindowComponents.hint_breakdown = "Hidden" if WindowComponents.active_user.hide_hint_breakdown else "Visible"

        if WindowComponents.max_score == "Visible": WindowComponents.hide_max_score_button.configure(text = "Visible", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        else: WindowComponents.hide_max_score_button.configure(text = "Hidden", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

        if WindowComponents.score_percentage == "Visible": WindowComponents.hide_score_percentage_button.configure(text = "Visible", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: WindowComponents.hide_score_percentage_button.configure(text = "Hidden", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        
        if WindowComponents.incorrect_count == "Visible": WindowComponents.hide_incorrect_count_button.configure(text = "Visible", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: WindowComponents.hide_incorrect_count_button.configure(text = "Hidden", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        
        if WindowComponents.question_percentage == "Visible": WindowComponents.hide_question_percentage_button.configure(text = "Visible", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        else: WindowComponents.hide_question_percentage_button.configure(text = "Hidden", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        
        if WindowComponents.hint_breakdown == "Visible": WindowComponents.hide_hint_breakdown_button.configure(text = "Visible", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        else: WindowComponents.hide_hint_breakdown_button.configure(text = "Hidden", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

    def set_hide_max_score() -> None:
        WindowComponents.max_score = "Hidden" if WindowComponents.max_score == "Visible" else "Visible"

        if WindowComponents.max_score == "Visible": WindowComponents.hide_max_score_button.configure(text = "Visible", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        else: WindowComponents.hide_max_score_button.configure(text = "Hidden", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

    def set_hide_score_percentage() -> None:
        WindowComponents.score_percentage = "Hidden" if WindowComponents.score_percentage == "Visible" else "Visible"
        
        if WindowComponents.score_percentage == "Visible": WindowComponents.hide_score_percentage_button.configure(text = "Visible", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: WindowComponents.hide_score_percentage_button.configure(text = "Hidden", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        
    def set_hide_incorrect_count() -> None:
        WindowComponents.incorrect_count = "Hidden" if WindowComponents.incorrect_count == "Visible" else "Visible"
        
        if WindowComponents.incorrect_count == "Visible": WindowComponents.hide_incorrect_count_button.configure(text = "Visible", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        else: WindowComponents.hide_incorrect_count_button.configure(text = "Hidden", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        
    def set_hide_question_percentage() -> None:
        WindowComponents.question_percentage = "Hidden" if WindowComponents.question_percentage == "Visible" else "Visible"
        
        if WindowComponents.question_percentage == "Visible": WindowComponents.hide_question_percentage_button.configure(text = "Visible", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        else: WindowComponents.hide_question_percentage_button.configure(text = "Hidden", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        
    def set_hide_hint_breakdown() -> None:
        WindowComponents.hint_breakdown = "Hidden" if WindowComponents.hint_breakdown == "Visible" else "Visible"
        
        if WindowComponents.hint_breakdown == "Visible": WindowComponents.hide_hint_breakdown_button.configure(text = "Visible", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        else: WindowComponents.hide_hint_breakdown_button.configure(text = "Hidden", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

    def update_leaderboard_settings() -> None:
        WindowComponents.active_user.hide_max_score = True if WindowComponents.max_score == "Hidden" else False
        WindowComponents.active_user.hide_score_percentage = True if WindowComponents.score_percentage == "Hidden" else False
        WindowComponents.active_user.hide_incorrect_count = True if WindowComponents.incorrect_count == "Hidden" else False
        WindowComponents.active_user.hide_questions_percentage = True if WindowComponents.question_percentage == "Hidden" else False
        WindowComponents.active_user.hide_hint_breakdown = True if WindowComponents.hint_breakdown == "Hidden" else False

        write_user_file(WindowComponents.active_user)

    def reset_leaderboard_settings() -> None:
        WindowComponents.max_score = "Visible"
        WindowComponents.score_percentage = "Hidden"
        WindowComponents.incorrect_count = "Hidden"
        WindowComponents.question_percentage = "Visible"
        WindowComponents.hint_breakdown = "Visible"

        WindowComponents.hide_max_score_button.configure(text = "Visible", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        WindowComponents.hide_score_percentage_button.configure(text = "Hidden", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        WindowComponents.hide_incorrect_count_button.configure(text = "Hidden", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        WindowComponents.hide_question_percentage_button.configure(text = "Visible", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        WindowComponents.hide_hint_breakdown_button.configure(text = "Visible", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
        

    # Clear Functions

    def clear_colour_selector() -> None: pass

    def clear_edit_accounts_page() -> None:
        WindowComponents.update_username_entry.delete(0, len(WindowComponents.update_username_entry.get()))
        WindowComponents.update_password_entry.delete(0, len(WindowComponents.update_password_entry.get()))
