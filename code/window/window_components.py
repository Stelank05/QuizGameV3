from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import PIL.Image
import PIL.ImageTk

from classes.audio import Audio
from classes.colour import Colour
from classes.player import Player
from classes.topic import Topic

from questions.question_base import BaseQuestion

from quiz.answer_past import PastAnswer

class WindowComponents:
    window: Tk

    active_user: Player
    current_edit_question: BaseQuestion = None
    current_edit_topic: Topic = None
    current_edit_colour: Colour = None
    current_edit_audio: Audio = None
    current_quiz: type = None


    # Pages

    #  Login + Account
    login_page: Toplevel = None
    create_account_page: Toplevel = None
    choose_colours: Toplevel = None
    view_account_page: Toplevel = None
    edit_account_page: Toplevel = None

    #  Home Page
    home_page: Toplevel = None

    #  Edit Pages
    edit_topic_page: Toplevel = None
    edit_colour_page: Toplevel = None
    edit_audio_page: Toplevel = None

    #  Quiz Pages
    edit_question_select_page: Toplevel = None
    edit_question_page: Toplevel = None
    image_preview_frame: Toplevel = None
    display_question_page: Toplevel = None
    question_view: Toplevel = None
    quiz_setup_page: Toplevel = None
    finish_quiz_page: Toplevel = None

    active_pages: list[Toplevel] = []


    # New Things

    #  Edit Topic Page Features
    topics_listbox: Listbox
    topic_name_entry: Entry
    topic_back_colour: StringVar
    topic_text_colour: StringVar
    contrast_output: Label
    topic_back: Colour
    topic_text: Colour

    #  Edit Colour Page Features
    colours_listbox: Listbox
    colour_name_entry: Entry
    colour_code_entry: Entry
    colour_output: Label

    #  Edit Audio Page Features
    audios_listbox: Listbox
    audio_name_entry: Entry
    audio_file_entry: Entry

    #  Edit Question Selector Features
    question_select_visible: bool = False

    current_question_set: Label
    question_list: Listbox

    current_display_type: str
    display_discarded: bool = False
    display_all: bool = True
    display_image_questions: bool = False

    chosen_question_type: StringVar
    chosen_question_topic: StringVar
    chosen_image_question: StringVar
    chosen_question_difficulty: StringVar
    chosen_question_usability: StringVar

    toggle_question_status: Button
    toggle_image_status: Button
    discard_question_button: Button

    question_types: list[str] = ["All", "Closed", "Open", "Order"]
    image_question_types: list[str] = ["All", "Image Question", "Text Only Question"]
    question_difficulties: list[str] = ["All", "Easy", "Medium", "Hard"]
    question_usabilities: list[str] = ["All", "Usable", "Discarded"]
    question_topics: list[str] = []

    question_keys: list[str] = []

    #  Question Editor Features
    preview_question_button: Button
    update_question_button: Button
    clear_question_details_button: Button

    # Page Path List
    page_path: list[str]


    # Default Colours + Font
    default_window_colours: list[Colour]
    default_button_colours: list[Colour]
    default_label_colours: list[Colour]
    default_entry_colours: list[Colour]
    #font: tuple[str, int]
    black: Colour
    white: Colour

    # User Colours
    window_colours: list[Colour]
    button_colours: list[Colour]
    label_colours: list[Colour]
    entry_colours: list[Colour]

    # Login Variables
    username_entry: Entry
    password_entry: Entry

    # Create Account Variables
    create_username_entry: Entry
    create_password_entry: Entry

    background_display: Label
    window_display: Label
    label_display: Label
    button_display: Button
    entry_display: Label

    # Update Account Variables
    update_username_entry: Entry
    update_password_entry: Entry

    ua_background_display: Label
    ua_window_display: Label
    ua_label_display: Label
    ua_button_display: Button
    ua_entry_display: Label

    # Login + Create Account Variables
    entered_username: str
    entered_password: str

    # Choose Colour Variables / Lists
    window_colour_widgets: list[Widget]
    button_colour_widgets: list[Widget]
    label_colour_widgets: list[Widget]
    entry_colour_widgets: list[Widget]

    # User Colour Selection
    window_back: StringVar
    window_text: StringVar
    select_window_back: ttk.Combobox
    select_window_text: ttk.Combobox

    label_back: StringVar
    label_text: StringVar
    select_label_back: ttk.Combobox
    select_label_text: ttk.Combobox

    button_back: StringVar
    button_text: StringVar
    select_button_back: ttk.Combobox
    select_button_text: ttk.Combobox

    entry_back: StringVar
    entry_text: StringVar
    select_entry_back: ttk.Combobox
    select_entry_text: ttk.Combobox

    chosen_window_text: Colour = None
    chosen_window_back: Colour = None
    chosen_button_back: Colour = None
    chosen_button_text: Colour = None
    chosen_label_back: Colour = None
    chosen_label_text: Colour = None
    chosen_entry_back: Colour = None
    chosen_entry_text: Colour = None

    chosen_colours: list[list[Colour]] = [[chosen_window_text, chosen_window_back],
                                          [chosen_button_text, chosen_button_back],
                                          [chosen_label_text, chosen_label_back],
                                          [chosen_entry_text, chosen_entry_back]]
    
    # Default Colours

    window_colours: list[Colour] = ["C0024", "C0001"]
    label_colours: list[Colour] = ["C0001", "C0002"]
    button_colours: list[Colour] = ["C0025", "C0002"]
    entry_colours: list[Colour] = ["C0025", "C0002"]
    minimum_contrast_ratio: float = 4.5
    main_font: tuple[str, int] = ["Calibri", 10]

    # Valid File Extensions
    # valid_audio_extensions: list[str] = [".wav", ".mp3", ".midi"]
    # vlaid_image_extensions: list[str] = ["jpg", "jpeg", "png"]

    # Hint Details
    text_hint_button: Button
    relevant_hint_button: Button
    image_question_button: Button

    add_text_hint: bool = True
    add_50_50_hint: bool = False
    add_provide_word_hint: bool = False
    add_place_one_hint: bool = False
    is_image_question: bool = False

    # Question Detail Entry Details
    question_text_input: Text
    text_hint_entry: Text
    relevant_hint_entry: Entry
    fun_fact_entry: Entry
    image_file_entry: Entry

    text_hint_header: Label

    # Answers
    answers: list[type] = []
    open_answer_required: Entry
    open_answer_acceptable: Entry

    # Other Details
    topic_selector: Listbox

    difficulty_selector: ttk.Combobox
    question_score_selector: ttk.Combobox
    chosen_difficulty: StringVar
    chosen_question_score: StringVar

    correct_audio_selector: ttk.Combobox
    incorrect_audio_selector: ttk.Combobox
    chosen_correct_audio: StringVar
    chosen_incorrect_audio: StringVar


    # Question View Details
    question_number_output: Label
    current_score_output: Label
    question_difficulty_output: Label
    filler_label: Label
    question_score_output: Label
    question_text_output: Label
    text_hint_output: Label
    question_image_output: Label
    topics_shroud: Label
    topics_shroud_header: Label
    fun_fact_preview: Label

    submit_answer: Button
    view_text_hint_button: Button
    view_relevant_hint_button: Button

    exit_quiz_button: Button
    review_last_question: Button
    review_next_question: Button
    next_question: Button

    closed_answers: list[Button] = []
    open_answer_entry: Text
    # Idk how I'm gonna do the Order Questions lol

    # UI Controls
    view_preview: Button
    view_image_preview: Button
    create_question: Button
    clear_window: Button
    back_button: Button
    centre_window: Button


    # Quiz Setup
    quiz_length_set: Scale

    topic_selection: Listbox

    include_closed_questions_button: Button
    include_open_questions_button: Button
    include_order_questions_button: Button
    
    include_easy_questions_button: Button
    include_medium_questions_button: Button
    include_hard_questions_button: Button

    include_image_questions_button: Button

    quiz_length: DoubleVar
    included_topics: list[str] = []
    # included_topic_ids: list[str] = []

    include_closed_questions: bool = True
    include_open_questions: bool = True
    include_order_questions: bool = False
    
    include_easy_questions: bool = True
    include_medium_questions: bool = True
    include_hard_questions: bool = True

    include_image_questions: bool = False

    available_questions: list[BaseQuestion] = []
    available_question_codes: list[str] = []

    # Play Quiz Button

    answers: list[PastAnswer]
    selected_answer: PastAnswer = None
    selected_button: Button = None

    open_hint_output: Label = None

    correct_answer_button: Button = None

    # Finish Quiz Frame Items
    permit_answer: bool # = True

    retake_quiz_button: Button
    review_quiz_button_finish: Button
    exit_quiz_button_finish: Button

    # Position Frame Function (I don't remember why I put it here but there probably was a reason)
    def position_frame(frame: Toplevel, frame_dimensions) -> None:
        x_offset: int = (frame.winfo_screenwidth() - frame_dimensions[0]) // 2
        y_offset: int = (frame.winfo_screenheight() - frame_dimensions[1]) // 2

        frame.geometry(f"{frame_dimensions[0]}x{frame_dimensions[1]}+{x_offset}+{y_offset}")
    
    def make_active(frame: Toplevel) -> None:
        frame.update()
        frame.deiconify()
