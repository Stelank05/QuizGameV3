import os

from tkinter import *
from tkinter import messagebox

from controls.colour_controls import ColourControls
from controls.file_handler import *
from controls.sort_functions import *

from questions.answer import Answer
from questions.question_base import BaseQuestion
from questions.question_closed import ClosedQuestion
from questions.question_open import OpenQuestion
from questions.question_order import OrderQuestion

from window.answer_creator import AnswerCreator
from window.window_components import WindowComponents

from common_data import CommonData

class QuestionController:
    question_file: str = ""
    image_file_location: str = ""

    # Create Questions

    def create_closed_question() -> None:
        if not QuestionController.valid_closed_question(): return 0
        
        # Image File Handling
        if WindowComponents.is_image_question:
            QuestionController.image_file_location = os.path.join(CommonData.images_folder, WindowComponents.image_file_entry.get().strip().split("\\")[-1])
            copy_image_file(WindowComponents.image_file_entry.get().strip(), QuestionController.image_file_location)
        else: QuestionController.image_file_location = ""

        question_dictionary: dict = QuestionController.create_closed_dict()
        
        QuestionController.question_file = os.path.join(CommonData.question_folder, f"{question_dictionary["Question ID"]}.json")
        
        write_json_file(QuestionController.question_file, question_dictionary)
        CommonData.usable_questions.append(ClosedQuestion(question_dictionary))

    def create_open_question() -> None:
        if not QuestionController.valid_open_question(): return 0
        
        # Image File Handling
        if WindowComponents.is_image_question:
            QuestionController.image_file_location = os.path.join(CommonData.images_folder, WindowComponents.image_file_entry.get().strip().split("\\")[-1])
            copy_image_file(WindowComponents.image_file_entry.get().strip(), QuestionController.image_file_location)
        else: QuestionController.image_file_location = ""

        question_dictionary: dict = QuestionController.create_open_dict()
        
        QuestionController.question_file = os.path.join(CommonData.question_folder, f"{question_dictionary["Question ID"]}.json")
        
        write_json_file(QuestionController.question_file, question_dictionary)
        CommonData.usable_questions.append(OpenQuestion(question_dictionary))
    
    def create_order_question() -> None: pass


    # Create Question Dictionaries

    def create_closed_dict() -> dict:
        return {
            "Question ID" : QuestionController.generate_question_id(),
            "Discarded Question": False,
            "Question Type" : "Closed",
            "Question Text" : WindowComponents.question_text_input.get("1.0", END)[:-1],
            "Question Difficulty" : WindowComponents.chosen_difficulty.get(),
            "Question Points" : WindowComponents.chosen_question_score.get(),
            "Question Topics" : QuestionController.compile_topic_list(),
            "Hints" : {
                "Add Text Hint" : WindowComponents.add_text_hint,
                "Text Hint" : WindowComponents.text_hint_entry.get("1.0", END)[:-1],
                "Add 50/50 Hint" : WindowComponents.add_50_50_hint
            },
            "Images" : {
                "Is Image Question" : WindowComponents.is_image_question,
                "Image File" : QuestionController.image_file_location
            },
            "Answers" : QuestionController.get_closed_answers(),
            "Fun Fact": WindowComponents.fun_fact_entry.get(),
            "Correct Audio" : CommonData.get_audio_from_name(WindowComponents.chosen_correct_audio.get(), 0, len(CommonData.audio_list)).audio_id,
            "Incorrect Audio" : CommonData.get_audio_from_name(WindowComponents.chosen_incorrect_audio.get(), 0, len(CommonData.audio_list)).audio_id
        }

    def create_open_dict() -> dict:
        return {
            "Question ID" : QuestionController.generate_question_id(),
            "Discarded Question": False,
            "Question Type" : "Open",
            "Question Text" : WindowComponents.question_text_input.get("1.0", END)[:-1],
            "Question Difficulty" : WindowComponents.chosen_difficulty.get(),
            "Question Points" : WindowComponents.chosen_question_score.get(),
            "Question Topics" : QuestionController.compile_topic_list(),
            "Hints" : {
                "Add Text Hint" : WindowComponents.add_text_hint,
                "Text Hint" : WindowComponents.text_hint_entry.get("1.0", END)[:-1],
                "Add Provide Word Hint" : WindowComponents.add_provide_word_hint,
                "Provided Word": WindowComponents.relevant_hint_entry.get()
            },
            "Images" : {
                "Is Image Question" : WindowComponents.is_image_question,
                "Image File" : QuestionController.image_file_location
            },
            "Answers" : QuestionController.get_open_answers(),
            "Fun Fact": WindowComponents.fun_fact_entry.get(),
            "Correct Audio" : CommonData.get_audio_from_name(WindowComponents.chosen_correct_audio.get(), 0, len(CommonData.audio_list)).audio_id,
            "Incorrect Audio" : CommonData.get_audio_from_name(WindowComponents.chosen_incorrect_audio.get(), 0, len(CommonData.audio_list)).audio_id
        }
    
    def create_order_dict() -> dict: pass


    # Create Partial Question Dictionaries

    def create_partial_closed_dict() -> dict:
        return {
            "Question Text" : WindowComponents.question_text_input.get("1.0", END)[:-1],
            "Question Difficulty" : WindowComponents.chosen_difficulty.get(),
            "Question Points" : WindowComponents.chosen_question_score.get(),
            "Question Topics" : QuestionController.compile_topic_list(),
            "Hints" : {
                "Add Text Hint" : WindowComponents.add_text_hint,
                "Text Hint" : WindowComponents.text_hint_entry.get("1.0", END)[:-1],
                "Add 50/50 Hint" : WindowComponents.add_50_50_hint
            },
            "Images" : {
                "Is Image Question" : WindowComponents.is_image_question,
                "Image File" : QuestionController.image_file_location
            },
            "Answers" : QuestionController.get_closed_answers(),
            "Fun Fact": WindowComponents.fun_fact_entry.get()
        }

    def create_partial_open_dict() -> dict:
        return {
            "Question Text" : WindowComponents.question_text_input.get("1.0", END)[:-1],
            "Question Difficulty" : WindowComponents.chosen_difficulty.get(),
            "Question Points" : WindowComponents.chosen_question_score.get(),
            "Question Topics" : QuestionController.compile_topic_list(),
            "Hints" : {
                "Add Text Hint" : WindowComponents.add_text_hint,
                "Text Hint" : WindowComponents.text_hint_entry.get("1.0", END)[:-1],
                "Add Provide Word Hint" : WindowComponents.add_provide_word_hint,
                "Provided Word": WindowComponents.relevant_hint_entry.get()
            },
            "Images" : {
                "Is Image Question" : WindowComponents.is_image_question,
                "Image File" : QuestionController.image_file_location
            },
            "Answers" : QuestionController.get_open_answers(),
            "Fun Fact": WindowComponents.fun_fact_entry.get()
        }
    
    def create_partial_order_dict() -> dict: pass


    # Create Answer Dictionaries

    def get_closed_answers() -> list[dict]:
        answers: list[dict] = []

        for i in range(len(WindowComponents.answers)):
            answer: AnswerCreator = WindowComponents.answers[i]

            if answer.include_answer:
                answers.append({
                    "Answer Text" : answer.answer_entry.get("1.0", END)[:-1],
                    "Answer Back Colour" : CommonData.get_colour_from_name(answer.selected_background.get(), 0, len(CommonData.colour_list)).colour_id,
                    "Answer Text Colour" : CommonData.get_colour_from_name(answer.selected_foreground.get(), 0, len(CommonData.colour_list)).colour_id,
                    "Correct Answer" : answer.correct_answer,
                    "Answer Number" : i + 1
                })

        return answers
    
    def get_open_answers() -> dict:
        return {
            "Required Words": list(set(WindowComponents.open_answer_required.get().lower().split(' '))),
            "Acceptable Words": list(set(WindowComponents.open_answer_acceptable.get().lower().split(' ')))
        }
    
    def get_order_answers() -> dict: pass


    # Update Questions
    
    def update_common_details() -> None:
        # Question Text
        WindowComponents.current_edit_question.question_text = WindowComponents.question_text_input.get("1.0", END)[:-1]

        # Hints
        WindowComponents.current_edit_question.add_text_hint = WindowComponents.add_text_hint
        WindowComponents.current_edit_question.text_hint = WindowComponents.text_hint_entry.get("1.0", END)[:-1]
        
        # Images
        WindowComponents.current_edit_question.is_image_question = WindowComponents.is_image_question,
        WindowComponents.current_edit_question.image_file = QuestionController.image_file_location

        # Fun Fact Text
        WindowComponents.current_edit_question.fun_fact = WindowComponents.fun_fact_entry.get()

        # Difficulty, Score + Audios
        WindowComponents.current_edit_question.question_difficulty = WindowComponents.chosen_difficulty.get()
        WindowComponents.current_edit_question.question_points = WindowComponents.chosen_question_score.get()
        WindowComponents.current_edit_question.correct_audio = CommonData.get_audio_from_name(WindowComponents.chosen_correct_audio.get(), 0, len(CommonData.audio_list)).audio_id
        WindowComponents.current_edit_question.incorrect_audio = CommonData.get_audio_from_name(WindowComponents.chosen_incorrect_audio.get(), 0, len(CommonData.audio_list)).audio_id

        # Topics
        WindowComponents.current_edit_question.question_topics = QuestionController.compile_topic_list()

    def update_closed_question() -> None:
        if not QuestionController.valid_closed_question(): return 0

        QuestionController.update_common_details()

        # WindowComponents.current_edit_question
        WindowComponents.current_edit_question.add_50_50_hint = WindowComponents.add_50_50_hint

        # Answers
        WindowComponents.current_edit_question.answers = QuestionController.get_closed_answers()

        QuestionController.question_file = os.path.join(CommonData.question_folder, f"{WindowComponents.current_edit_question.question_id}.json")
        write_json_file(QuestionController.question_file, WindowComponents.current_edit_question.create_dictionary())

    def update_open_question() -> None:
        if not QuestionController.valid_open_question(): return 0

        QuestionController.update_common_details()

        # WindowComponents.current_edit_question
        WindowComponents.current_edit_question.add_provide_word_hint = WindowComponents.add_provide_word_hint
        WindowComponents.current_edit_question.provided_word = WindowComponents.relevant_hint_entry.get()

        QuestionController.question_file = os.path.join(CommonData.question_folder, f"{WindowComponents.current_edit_question.question_id}.json")
        write_json_file(QuestionController.question_file, WindowComponents.current_edit_question.create_dictionary())

    def update_order_question() -> None: pass


    # Validation

    def valid_details() -> bool:
        # Valid Question Text
        if WindowComponents.question_text_input.get("1.0", END).strip() == "":
            messagebox.showerror("Invalid Question Text", "Please Enter a Question")
            return False
        
        # Valid Image File
        if WindowComponents.is_image_question:
            if not QuestionController.valid_image_file():
                messagebox.showerror("Invalid Image File", "The provided Image File is Invalid")
                return False
        
        # Valid Text Hint
        if WindowComponents.add_text_hint and WindowComponents.text_hint_entry.get("1.0", END).strip() == "":
            messagebox.showerror("Invalid Text Hint", "Text Hint is Selected, but No Hint is given")
            return False
        
        # Topics Selected
        if len(WindowComponents.topic_selector.curselection()) < 1:
            messagebox.showerror("No Topics Selected", "Please Select at Least 1 Topic")
            return False
        
        if len(QuestionController.compile_topic_list()) > 7:
            messagebox.showerror("Too Many Topics", "A Question can only contain up to 6 Topic Tags")
            return False

        # Question Difficulty Selected
        if WindowComponents.chosen_difficulty.get() == "Question Difficulty":
            messagebox.showerror("No Difficulty Selected", "Please Select a Question Difficulty")
            return False

        # Question Score Selected
        if WindowComponents.chosen_question_score.get() == "Question Score":
            messagebox.showerror("No Question Score Selected", "Please Select a Question Score")
            return False

        # Correct Audio Selected
        if WindowComponents.chosen_correct_audio.get() == "Correct Audio":
            messagebox.showerror("No Correct Audio Selected", "Please Select a 'Correct Audio'")
            return False

        # Incorrect Audio Selected
        if WindowComponents.chosen_correct_audio.get() == "Incorrect Audio":
            messagebox.showerror("No Incorrect Audio Selected", "Please Select a 'Incorrect Audio'")
            return False
        
        # Both Audio Files the Same
        if WindowComponents.chosen_correct_audio.get() == WindowComponents.chosen_incorrect_audio.get():
            messagebox.showerror("Same Audios", "Please Select Unique Audios for 'Correct Audio' and 'Incorrect Audio'")
            return False

        return True
        
    def valid_closed_question() -> bool:
        answer_count: int = 0
        correct_answer_count: int = 0

        if not QuestionController.valid_details(): return False

        # Valid Answers
        for answer in WindowComponents.answers:
            if answer.include_answer:
                answer_count += 1

                if not answer.valid_answer():
                    messagebox.showerror("Invalid Answer", f"You have an Invalid Answer for Answer {answer.answer_number}")
                    return False
                
                if answer.selected_background.get() in ["Red", "Green", "Indigo"]:
                    messagebox.showerror("Invalid Background Colour", f"You have an Invalid Answer Background for Answer {answer.answer_number}")
                    return False
                
                if not ColourControls.check_contrast_ratio(CommonData.get_colour_from_name(answer.selected_background.get(), 0, len(CommonData.colour_list)).luminance, CommonData.get_colour_from_name(answer.selected_foreground.get(), 0, len(CommonData.colour_list)).luminance):
                    messagebox.showerror("Invalid Colour Contrast Ratio", f"You have an Invalid Answer Contrast Ratio for Answer {answer.answer_number}")
                    return False

                if answer.correct_answer: correct_answer_count += 1

        # Valid Answers
        if correct_answer_count == 0:
            messagebox.showerror("No Correct Answer", "A Correct Answer hasn't been set")
            return False
        
        if correct_answer_count > 1:
            messagebox.showerror("Multiple Correct Answers", "You have set Multiple Answers as Correct")
            return False
        
        if answer_count < 2:
            messagebox.showerror("Insufficient Answers", "You Must have at least 2 Answers for a Question")
            return False
        
        return True

    def valid_open_question() -> bool:
        requireds: list[str] = WindowComponents.open_answer_required.get().upper().split(' ')
        acceptables: list[str] = WindowComponents.open_answer_acceptable.get().upper().split(' ')

        for required in requireds:
            if required in acceptables:
                messagebox.showerror("Duplicate Word", "Word in Required Words also in Acceptable Words")
                return False

        if WindowComponents.add_provide_word_hint and WindowComponents.relevant_hint_entry.get().upper() not in requireds:
            messagebox.showerror("Invalid Provided Word", "Provided Word not in Required Words")
            return False

        return True

    def valid_order_question() -> bool: return False

    def valid_image_file() -> bool:
        file_path: str = WindowComponents.image_file_entry.get().strip()

        if not os.path.exists(file_path): return False
        if not file_path.lower().endswith(("jpg", "jpeg", "png")): return False
        return True
    

    # Miscellaneous Functions

    def generate_question_id() -> str:
        last_id: str = ""

        if len(CommonData.usable_questions) == 0 and len(CommonData.discarded_questions) == 0: return "Q0001"
        elif len(CommonData.usable_questions) > 0 and len(CommonData.discarded_questions) == 0: last_id = CommonData.usable_questions[-1].question_id
        elif len(CommonData.usable_questions) == 0 and len(CommonData.discarded_questions) > 0: last_id = CommonData.discarded_questions[-1].question_id
        elif (CommonData.usable_questions[-1].question_id > CommonData.discarded_questions[-1].question_id): last_id = CommonData.usable_questions[-1].question_id
        else: last_id = CommonData.discarded_questions[-1].question_id

        new_id: str = f"Q{str(int(last_id.replace("Q", "")) + 1).rjust(4, "0")}"

        return new_id

    def compile_topic_list() -> list[str]:
        topic_list: list[str] = []

        id_sort_topics(CommonData.topic_list)

        for topic in WindowComponents.topic_selector.curselection():
            topic_list.append(CommonData.topic_list[topic].topic_id)

        return topic_list