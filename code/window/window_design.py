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

from questions.question_closed import ClosedQuestion
from questions.question_open import OpenQuestion
from questions.question_order import OrderQuestion

from quiz.quiz import Quiz

from window.answer_creator import AnswerCreator
from window.question_design import QuestionDesign
from window.window_components import WindowComponents
from window.window_controls import WindowControls

from common_data import CommonData

class WindowDesign:
    def create_login_page() -> None:
        WindowComponents.login_page = Toplevel(WindowComponents.window)

        WindowComponents.window.withdraw()

        frame_width: int = 225
        frame_height: int = 370

        WindowComponents.login_page.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.login_page.config(bg = WindowComponents.default_window_colours[0].colour_code)

        WindowComponents.position_frame(WindowComponents.login_page, [frame_width, frame_height])
        WindowComponents.make_active(WindowComponents.login_page)

        header_label: Label = Label(WindowComponents.login_page, text = "Login Page", bg = WindowComponents.default_label_colours[0].colour_code, fg = WindowComponents.default_label_colours[1].colour_code, font = WindowComponents.main_font)
        header_label.place(x = 25, y = 25, width = 175, height = 30)

        username_header: Label = Label(WindowComponents.login_page, text = "Username", bg = WindowComponents.default_window_colours[0].colour_code, fg = WindowComponents.default_window_colours[1].colour_code, font = WindowComponents.main_font)
        username_header.place(x = 25, y = 70, width = 175, height = 20)

        WindowComponents.username_entry = Entry(WindowComponents.login_page, bg = WindowComponents.default_entry_colours[0].colour_code, fg = WindowComponents.default_entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.username_entry.place(x = 25, y = 95, width = 175, height = 30)

        password_header: Label = Label(WindowComponents.login_page, text = "Password", bg = WindowComponents.default_window_colours[0].colour_code, fg = WindowComponents.default_window_colours[1].colour_code, font = WindowComponents.main_font)
        password_header.place(x = 25, y = 140, width = 175, height = 20)

        WindowComponents.password_entry = Entry(WindowComponents.login_page, bg = WindowComponents.default_entry_colours[0].colour_code, fg = WindowComponents.default_entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.password_entry.place(x = 25, y = 165, width = 175, height = 30)

        login_button: Button = Button(WindowComponents.login_page, text = "Login", bg = WindowComponents.default_button_colours[0].colour_code, fg = WindowComponents.default_button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowDesign.attempt_login)
        login_button.place(x = 25, y = 210, width = 175, height = 30)

        create_account_button: Button = Button(WindowComponents.login_page, text = "Create Account", bg = WindowComponents.default_button_colours[0].colour_code, fg = WindowComponents.default_button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Login Page", "Create Account"))
        create_account_button.place(x = 25, y = 245, width = 175, height = 30)

        login_as_guest_button: Button = Button(WindowComponents.login_page, text = "Login as Guest", bg = WindowComponents.default_button_colours[0].colour_code, fg = WindowComponents.default_button_colours[1].colour_code, font = WindowComponents.main_font)#, command = WindowDesign.login_as_guest)
        login_as_guest_button.place(x = 25, y = 280, width = 175, height = 30)

        exit_button: Button = Button(WindowComponents.login_page, text = "Exit", bg = WindowComponents.default_button_colours[0].colour_code, fg = WindowComponents.default_button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(exit_app, WindowComponents.window))
        exit_button.place(x = 25, y = 315, width = 175, height = 30)

    def create_create_account_page() -> None:
        WindowComponents.login_page.withdraw()
        WindowComponents.create_account_page = Toplevel(WindowComponents.window)

        frame_width: int = 445
        frame_height: int = 380

        WindowComponents.create_account_page.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.create_account_page.config(bg = WindowComponents.default_window_colours[0].colour_code)

        WindowComponents.position_frame(WindowComponents.create_account_page, [frame_width, frame_height])
        WindowComponents.make_active(WindowComponents.create_account_page)

        login_header: Label = Label(WindowComponents.create_account_page, text = "Create Account Page", bg = WindowComponents.default_label_colours[0].colour_code, fg = WindowComponents.default_label_colours[1].colour_code, font = WindowComponents.main_font)
        login_header.place(x = 25, y = 25, width = 175, height = 30)

        username_header: Label = Label(WindowComponents.create_account_page, text = "Username", bg = WindowComponents.default_window_colours[0].colour_code, fg = WindowComponents.default_window_colours[1].colour_code, font = WindowComponents.main_font)
        username_header.place(x = 25, y = 70, width = 175, height = 20)

        WindowComponents.create_username_entry = Entry(WindowComponents.create_account_page, bg = WindowComponents.default_entry_colours[0].colour_code, fg = WindowComponents.default_entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.create_username_entry.place(x = 25, y = 95, width = 175, height = 30)

        password_header: Label = Label(WindowComponents.create_account_page, text = "Password", bg = WindowComponents.default_window_colours[0].colour_code, fg = WindowComponents.default_window_colours[1].colour_code, font = WindowComponents.main_font)
        password_header.place(x = 25, y = 140, width = 175, height = 20)

        WindowComponents.create_password_entry = Entry(WindowComponents.create_account_page, bg = WindowComponents.default_entry_colours[0].colour_code, fg = WindowComponents.default_entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.create_password_entry.place(x = 25, y = 165, width = 175, height = 30)


        # Colour stuffs

        ColourControls.reset_colours()

        choose_colours_button: Button = Button(WindowComponents.create_account_page, text = "Choose Colours", bg = WindowComponents.default_button_colours[0].colour_code, fg = WindowComponents.default_button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.open_colour_selector, "Create Account"))
        choose_colours_button.place(x = 25, y = 220, width = 175, height = 30)

        colours_border: Label = Label(WindowComponents.create_account_page, bg = "#000000")
        colours_border.place(x = 225, y = 25, width = 195, height = 330)

        WindowComponents.background_display = Label(WindowComponents.create_account_page, bg = WindowComponents.window_colours[0].colour_code)
        WindowComponents.background_display.place(x = 240, y = 40, width = 165, height = 300)

        WindowComponents.window_display = Label(WindowComponents.create_account_page, text = "Window Colours", bg = WindowComponents.window_colours[0].colour_code, fg = WindowComponents.window_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.window_display.place(x = 255, y = 55, width = 135, height = 45)

        WindowComponents.label_display = Label(WindowComponents.create_account_page, text = "Label Colours", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.label_display.place(x = 255, y = 115, width = 135, height = 60)

        WindowComponents.button_display = Button(WindowComponents.create_account_page, text = "Button Colours", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.button_display.place(x = 255, y = 190, width = 135, height = 60)

        WindowComponents.entry_display = Label(WindowComponents.create_account_page, text = "Entry Colours", bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.entry_display.place(x = 255, y = 265, width = 135, height = 60)


        # Control Buttons

        create_account_button: Button = Button(WindowComponents.create_account_page, text = "Create Account", bg = WindowComponents.default_button_colours[0].colour_code, fg = WindowComponents.default_button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowDesign.create_account)
        create_account_button.place(x = 25, y = 255, width = 175, height = 30)

        back_button: Button = Button(WindowComponents.create_account_page, text = "Back", bg = WindowComponents.default_button_colours[0].colour_code, fg = WindowComponents.default_button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Create Account", "Login Page"))
        back_button.place(x = 25, y = 290, width = 175, height = 30)

        exit_button: Button = Button(WindowComponents.create_account_page, text = "Exit", bg = WindowComponents.default_button_colours[0].colour_code, fg = WindowComponents.default_button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(exit_app, WindowComponents.window))
        exit_button.place(x = 25, y = 325, width = 175, height = 30)

    def create_choose_colours_page(selector_type: str) -> None:
        WindowComponents.choose_colours = Toplevel(WindowComponents.window)

        frame_width: int = 725
        frame_height: int = 400

        WindowComponents.choose_colours.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.choose_colours.config(bg = WindowComponents.default_window_colours[0].colour_code)

        WindowComponents.position_frame(WindowComponents.choose_colours, [frame_width, frame_height])
        WindowComponents.make_active(WindowComponents.choose_colours)

        WindowDesign.create_colour_selector(WindowComponents.choose_colours, selector_type, "Window", 25, 25)
        WindowDesign.create_colour_selector(WindowComponents.choose_colours, selector_type, "Button", 200, 25)
        WindowDesign.create_colour_selector(WindowComponents.choose_colours, selector_type, "Label", 375, 25)
        WindowDesign.create_colour_selector(WindowComponents.choose_colours, selector_type, "Entry", 550, 25)
        
        # Reset Colour Options
        reset_colour_options: Button = Button(WindowComponents.choose_colours, text = "Reset Colours", bg = WindowComponents.default_button_colours[0].colour_code, fg = WindowComponents.default_button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(ColourControls.reset_colour_options, selector_type))
        reset_colour_options.place(x = 25, y = 25 + (2 * (30 + 15) + (2 * (30 + 25))) + (2 * (15 + 45)), width = 325, height = 30)

        # Select Colour Options
        select_colour_options: Button = Button(WindowComponents.choose_colours, text = "Select Colours", bg = WindowComponents.default_button_colours[0].colour_code, fg = WindowComponents.default_button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(ColourControls.select_colours, WindowComponents.choose_colours, selector_type))
        select_colour_options.place(x = 375, y = 25 + (2 * (30 + 15) + (2 * (30 + 25))) + (2 * (15 + 45)), width = 325, height = 30)

    def create_colour_selector(frame: Toplevel, selector_type: str, header: str, start_x: int, start_y: int) -> None:
        background_header: Label = Label(frame, text = f"{header} Background Colour", wraplength = 130, bg = WindowComponents.default_window_colours[0].colour_code, fg = WindowComponents.default_window_colours[1].colour_code, font = WindowComponents.main_font)
        background_header.place(x = start_x, y = start_y, width = 150, height = 30)

        background_selector: ttk.ComboBox = ttk.Combobox(frame)
        background_selector['values'] = CommonData.colour_names
        background_selector['state'] = 'readonly'
        background_selector.place(x = start_x, y = start_y + (30 + 15), width = 150, height = 30)

        foreground_header: Label = Label(frame, text = f"{header} Foreground Colour", wraplength = 130, bg = WindowComponents.default_window_colours[0].colour_code, fg = WindowComponents.default_window_colours[1].colour_code, font = WindowComponents.main_font)
        foreground_header.place(x = start_x, y = start_y + (30 + 15) + (30 + 25), width = 150, height = 30)

        foreground_selector: ttk.ComboBox = ttk.Combobox(frame)
        foreground_selector['values'] = CommonData.colour_names
        foreground_selector['state'] = 'readonly'
        foreground_selector.place(x = start_x, y = start_y + (2 * (30 + 15)) + (30 + 25), width = 150, height = 30)

        contrast_ratio_output: Label = Label(frame, text = "Contrast Ratio: Something", wraplength = 130, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        contrast_ratio_output.place(x = start_x, y = start_y + (2 * (30 + 15) + (2 * (30 + 25))), width = 150, height = 45)

        set_contrast_ratio_button: Button = Button(frame, text = "Calculate Colour Contrast Ratio", wraplength = 130, bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(ColourControls.set_contrast_ratio, header, contrast_ratio_output))
        set_contrast_ratio_button.place(x = start_x, y = start_y + (2 * (30 + 15) + (2 * (30 + 25))) + (15 + 45), width = 150, height = 45)

        set_back: str; set_text: str
        [set_back, set_text] = ColourControls.get_set_colours(selector_type, header)

        if selector_type == "Update User Colours": contrast_ratio_output.configure(text = f"Contrast Ratio:\n{ColourControls.get_contrast_ratio(set_back.luminance, set_text.luminance)}", bg = set_back.colour_code, fg = set_text.colour_code)

        match header:
            case "Window":
                WindowComponents.window_back = StringVar()
                WindowComponents.window_text = StringVar()

                background_selector.configure(textvariable = WindowComponents.window_back)
                foreground_selector.configure(textvariable = WindowComponents.window_text)

                WindowComponents.window_back.set(set_back.colour_name)
                WindowComponents.window_text.set(set_text.colour_name)
            case "Button":
                WindowComponents.button_back = StringVar()
                WindowComponents.button_text = StringVar()

                background_selector.configure(textvariable = WindowComponents.button_back)
                foreground_selector.configure(textvariable = WindowComponents.button_text)

                WindowComponents.button_back.set(set_back.colour_name)
                WindowComponents.button_text.set(set_text.colour_name)
            case "Label":
                WindowComponents.label_back = StringVar()
                WindowComponents.label_text = StringVar()

                background_selector.configure(textvariable = WindowComponents.label_back)
                foreground_selector.configure(textvariable = WindowComponents.label_text)

                WindowComponents.label_back.set(set_back.colour_name)
                WindowComponents.label_text.set(set_text.colour_name)
            case "Entry":
                WindowComponents.entry_back = StringVar()
                WindowComponents.entry_text = StringVar()

                background_selector.configure(textvariable = WindowComponents.entry_back)
                foreground_selector.configure(textvariable = WindowComponents.entry_text)

                WindowComponents.entry_back.set(set_back.colour_name)
                WindowComponents.entry_text.set(set_text.colour_name)

    def create_home_page() -> None:
        WindowComponents.home_page = Toplevel(WindowComponents.window)
        WindowComponents.active_pages.append(WindowComponents.home_page)
        
        ColourControls.set_user_colours()

        frame_width: int = 410
        frame_height: int = 280

        WindowComponents.home_page.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.home_page.config(bg = WindowComponents.window_colours[0].colour_code)

        WindowComponents.position_frame(WindowComponents.home_page, [frame_width, frame_height])
        WindowComponents.make_active(WindowComponents.home_page)

        username_label: Label = Label(WindowComponents.home_page, text = f"Username: {WindowComponents.active_user.username}", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        username_label.place(x = 25, y = 25, width = 175, height = 30)

        high_score_label: Label = Label(WindowComponents.home_page, text = f"High Score: {WindowComponents.active_user.high_score}", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        high_score_label.place(x = 210, y = 25, width = 175, height = 30)

        play_quiz_button: Button = Button(WindowComponents.home_page, text = "Play Quiz", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Home Page", "Setup Quiz"))
        play_quiz_button.place(x = 25, y = 65, width = 360, height = 30)

        edit_questions_button: Button = Button(WindowComponents.home_page, text = "Edit Questions", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Home Page", "Edit Question Selector"))
        edit_questions_button.place(x = 25, y = 105, width = 175, height = 30)

        edit_topics_button: Button = Button(WindowComponents.home_page, text = "Edit Topics", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Home Page", "Edit Topics"))
        edit_topics_button.place(x = 210, y = 105, width = 175, height = 30)

        edit_colours_button: Button = Button(WindowComponents.home_page, text = "Edit Colours", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Home Page", "Edit Colours"))
        edit_colours_button.place(x = 25, y = 145, width = 175, height = 30)

        edit_audios_button: Button = Button(WindowComponents.home_page, text = "Edit Audios", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Home Page", "Edit Audios"))
        edit_audios_button.place(x = 210, y = 145, width = 175, height = 30)

        edit_user_account_button: Button = Button(WindowComponents.home_page, text = "View Account", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Home Page", "View Account"))
        edit_user_account_button.place(x = 25, y = 185, width = 175, height = 30)

        view_leaderboard_button: Button = Button(WindowComponents.home_page, text = "View Leaderboard", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Home Page", "View Leaderboard"))
        view_leaderboard_button.place(x = 210, y = 185, width = 175, height = 30)

        logout_button: Button = Button(WindowComponents.home_page, text = "Logout", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowDesign.logout)
        logout_button.place(x = 25, y = 225, width = 115, height = 30)

        centre_window: Button = Button(WindowComponents.home_page, text = "Center", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowComponents.position_frame, WindowComponents.home_page, [frame_width, frame_height]))
        centre_window.place(x = 150, y = 225, width = 110, height = 30)

        exit_button: Button = Button(WindowComponents.home_page, text = "Exit App", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(exit_app, WindowComponents.window))
        exit_button.place(x = 270, y = 225, width = 115, height = 30)

    def create_quiz_setup_page() -> None:
        WindowComponents.quiz_setup_page = Toplevel(WindowComponents.window)
        WindowComponents.active_pages.append(WindowComponents.home_page)
        
        ColourControls.set_user_colours()

        frame_width: int = 585
        frame_height: int = 360

        WindowComponents.quiz_setup_page.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.quiz_setup_page.config(bg = WindowComponents.window_colours[0].colour_code)

        WindowComponents.position_frame(WindowComponents.quiz_setup_page, [frame_width, frame_height])
        WindowComponents.make_active(WindowComponents.quiz_setup_page)

        # Chosen Topics
        topics_header: Label = Label(WindowComponents.quiz_setup_page, text = "Select Question Topics", bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        topics_header.place(x = 25, y = 25, width = 175, height = 30)

        WindowComponents.topic_selection = Listbox(WindowComponents.quiz_setup_page, selectmode = 'multiple', exportselection = False, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.topic_selection.place(x = 25, y = 60, width = 175, height = 205)
        WindowComponents.topic_selection.bind("<<ListboxSelect>>", WindowControls.update_quiz_topics)

        id_sort_topics(CommonData.topic_list)
        for topic in CommonData.topic_list: WindowComponents.topic_selection.insert('end', f"{topic.topic_id} - {topic.topic_name}")

        # Chosen Question Types
        type_header: Label = Label(WindowComponents.quiz_setup_page, text = "Select Question Types", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        type_header.place(x = 205, y = 25, width = 175, height = 30)

        WindowComponents.include_closed_questions_button = Button(WindowComponents.quiz_setup_page, text = f"Add Closed Questions: {WindowComponents.include_closed_questions}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowControls.toggle_question_type, "Closed"))
        WindowComponents.include_closed_questions_button.place(x = 205, y = 60, width = 175, height = 30)
        
        WindowComponents.include_open_questions_button = Button(WindowComponents.quiz_setup_page, text = f"Add Open Questions: {WindowComponents.include_open_questions}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowControls.toggle_question_type, "Open"))
        WindowComponents.include_open_questions_button.place(x = 205, y = 95, width = 175, height = 30)
        
        WindowComponents.include_order_questions_button = Button(WindowComponents.quiz_setup_page, text = f"Add Order Questions: {WindowComponents.include_order_questions}", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code, font = WindowComponents.main_font) # , command = functools.partial(WindowControls.toggle_question_type, "Order"))
        WindowComponents.include_order_questions_button.place(x = 205, y = 130, width = 175, height = 30)

        # Chosen Difficulty (/ies)
        type_header: Label = Label(WindowComponents.quiz_setup_page, text = "Select Question Types", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        type_header.place(x = 385, y = 25, width = 175, height = 30)

        WindowComponents.include_easy_questions_button = Button(WindowComponents.quiz_setup_page, text = f"Add Easy Questions: {WindowComponents.include_easy_questions}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowControls.toggle_question_difficulty, "Easy"))
        WindowComponents.include_easy_questions_button.place(x = 385, y = 60, width = 175, height = 30)
        
        WindowComponents.include_medium_questions_button = Button(WindowComponents.quiz_setup_page, text = f"Add Medium Questions: {WindowComponents.include_medium_questions}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowControls.toggle_question_difficulty, "Medium"))
        WindowComponents.include_medium_questions_button.place(x = 385, y = 95, width = 175, height = 30)
        
        WindowComponents.include_hard_questions_button = Button(WindowComponents.quiz_setup_page, text = f"Add Hard Questions: {WindowComponents.include_hard_questions}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowControls.toggle_question_difficulty, "Hard"))
        WindowComponents.include_hard_questions_button.place(x = 385, y = 130, width = 175, height = 30)

        # Toggle Images
        WindowComponents.include_image_questions_button = Button(WindowComponents.quiz_setup_page, text = f"Include Image Questions: {WindowComponents.include_image_questions}", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code, font = WindowComponents.main_font) # , command = WindowControls.toggle_include_images)
        WindowComponents.include_image_questions_button.place(x = 205, y = 165, width = 355, height = 30)

        # Quiz Length
        quiz_length_header: Label = Label(WindowComponents.quiz_setup_page, text = "Select Quiz Length", bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        quiz_length_header.place(x = 205, y = 200, width = 355, height = 30)

        WindowComponents.quiz_length = DoubleVar()
        WindowComponents.quiz_length_set = Scale(WindowComponents.quiz_setup_page, variable = WindowComponents.quiz_length, from_ = 0, to = 0, orient = HORIZONTAL, bg = WindowComponents.window_colours[0].colour_code, fg = WindowComponents.window_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.quiz_length_set.place(x = 205, y = 235, width = 355, height = 30)

        # Play Quiz Button
        begin_quiz: Button = Button(WindowComponents.quiz_setup_page, text = "Begin Quiz", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowControls.setup_quiz)
        begin_quiz.place(x = 25, y = 270, width = 535, height = 30)

        # Generic Controls
        back_button: Button = Button(WindowComponents.quiz_setup_page, text = "Back", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Setup Quiz", "Home Page"))
        back_button.place(x = 25, y = 305, width = 175, height = 30)

        centre_window: Button = Button(WindowComponents.quiz_setup_page, text = "Center", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowComponents.position_frame, WindowComponents.quiz_setup_page, [frame_width, frame_height]))
        centre_window.place(x = 205, y = 305, width = 175, height = 30)

        clear_quiz_settings: Button = Button(WindowComponents.quiz_setup_page, text = "Clear Selected Settings", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowControls.clear_quiz_settings)
        clear_quiz_settings.place(x = 385, y = 305, width = 175, height = 30)

    def create_edit_question_selector_page() -> None:
        WindowComponents.edit_question_select_page = Toplevel(WindowComponents.window)
        WindowComponents.active_pages.append(WindowComponents.edit_question_select_page)
        
        ColourControls.set_user_colours()

        frame_width: int = 605
        frame_height: int = 290

        WindowComponents.edit_question_select_page.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.edit_question_select_page.config(bg = WindowComponents.window_colours[0].colour_code)

        WindowComponents.position_frame(WindowComponents.edit_question_select_page, [frame_width, frame_height])
        WindowComponents.make_active(WindowComponents.edit_question_select_page)

        WindowComponents.current_question_set = Label(WindowComponents.edit_question_select_page, text = "Select Question", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.current_question_set.place(x = 25, y = 25, width = 175, height = 30)

        WindowComponents.question_list = Listbox(WindowComponents.edit_question_select_page, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.question_list.place(x = 25, y = 60, width = 175, height = 170)
        WindowComponents.question_list.bind("<<ListboxSelect>>", WindowControls.update_discard_button)

        # Left Controls

        back_button: Button = Button(WindowComponents.edit_question_select_page, text = "Back", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Edit Question Selector", "Home Page"))
        back_button.place(x = 25, y = 235, width = 85, height = 30)

        centre_window: Button = Button(WindowComponents.edit_question_select_page, text = "Center", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowComponents.position_frame, WindowComponents.edit_question_select_page, [frame_width, frame_height]))
        centre_window.place(x = 115, y = 235, width = 85, height = 30)

        clear_question_list: Button = Button(WindowComponents.edit_question_select_page, text = "Clear List", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowControls.clear_question_list)
        clear_question_list.place(x = 215, y = 235, width = 175, height = 30)

        view_questions: Button = Button(WindowComponents.edit_question_select_page, text = "Display Questions", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, command = WindowControls.display_questions)
        view_questions.place(x = 405, y = 235, width = 175, height = 30)

        display_controls_label: Label = Label(WindowComponents.edit_question_select_page, text = "Question Selection Controls", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        display_controls_label.place(x = 215, y = 25, width = 175, height = 30)

        # Question Types
        choose_question_type: ttk.Combobox = ttk.Combobox(WindowComponents.edit_question_select_page)
        choose_question_type['values'] = WindowComponents.question_types
        choose_question_type['state'] = 'readonly'
        choose_question_type.place(x = 215, y = 60, width = 175, height = 30)
        WindowComponents.chosen_question_type = StringVar()
        choose_question_type.configure(textvariable = WindowComponents.chosen_question_type)
        WindowComponents.chosen_question_type.set("Question Type")
        
        # Question Topics - Needs to be a Listbox or something
        WindowComponents.question_topics = ["All"] + WindowControls.get_topic_name_list()
        choose_question_topic: ttk.Combobox = ttk.Combobox(WindowComponents.edit_question_select_page)
        choose_question_topic['values'] = WindowComponents.question_topics
        choose_question_topic['state'] = 'readonly'
        choose_question_topic.place(x = 215, y = 95, width = 175, height = 30)
        WindowComponents.chosen_question_topic = StringVar()
        choose_question_topic.configure(textvariable = WindowComponents.chosen_question_topic)
        WindowComponents.chosen_question_topic.set("Question Topic")

        # Image Questions
        choose_image_question: ttk.Combobox = ttk.Combobox(WindowComponents.edit_question_select_page)
        choose_image_question['values'] = WindowComponents.image_question_types
        choose_image_question['state'] = 'readonly'
        choose_image_question.place(x = 215, y = 130, width = 175, height = 30)
        WindowComponents.chosen_image_question = StringVar()
        choose_image_question.configure(textvariable = WindowComponents.chosen_image_question)
        WindowComponents.chosen_image_question.set("Image Question")

        # Question Difficulties
        choose_question_difficulty: ttk.Combobox = ttk.Combobox(WindowComponents.edit_question_select_page)
        choose_question_difficulty['values'] = WindowComponents.question_difficulties
        choose_question_difficulty['state'] = 'readonly'
        choose_question_difficulty.place(x = 215, y = 165, width = 175, height = 30)
        WindowComponents.chosen_question_difficulty = StringVar()
        choose_question_difficulty.configure(textvariable = WindowComponents.chosen_question_difficulty)
        WindowComponents.chosen_question_difficulty.set("Question Difficulty")

        # Question Difficulties
        choose_question_usability: ttk.Combobox = ttk.Combobox(WindowComponents.edit_question_select_page)
        choose_question_usability['values'] = WindowComponents.question_usabilities
        choose_question_usability['state'] = 'readonly'
        choose_question_usability.place(x = 215, y = 200, width = 175, height = 30)
        WindowComponents.chosen_question_usability = StringVar()
        choose_question_usability.configure(textvariable = WindowComponents.chosen_question_usability)
        WindowComponents.chosen_question_usability.set("Question Usability")

        question_control_header: Label = Label(WindowComponents.edit_question_select_page, text = "Question Controls", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        question_control_header.place(x = 405, y = 25, width = 175, height = 30)

        create_closed_question_button: Button = Button(WindowComponents.edit_question_select_page, text = "Create Closed Question", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Edit Question Selector", "Create Closed Question", True))
        create_closed_question_button.place(x = 405, y = 60, width = 175, height = 30)

        create_open_question_button: Button = Button(WindowComponents.edit_question_select_page, text = "Create Open Question", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Edit Question Selector", "Create Open Question", True))
        create_open_question_button.place(x = 405, y = 95, width = 175, height = 30)

        create_order_question_button: Button = Button(WindowComponents.edit_question_select_page, text = "Create Order Question", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Edit Question Selector", "Create Order Question", True))
        create_order_question_button.place(x = 405, y = 130, width = 175, height = 30)
        
        edit_question_button: Button = Button(WindowComponents.edit_question_select_page, text = "Edit Question", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowDesign.open_edit_question)
        edit_question_button.place(x = 405, y = 165, width = 175, height = 30)

        WindowComponents.discard_question_button = Button(WindowComponents.edit_question_select_page, text = "Discard Question", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.discard_question_button.place(x = 405, y = 200, width = 175, height = 30)

        WindowControls.display_all_questions()

    def create_edit_topic_page() -> None:
        WindowComponents.edit_topic_page = Toplevel(WindowComponents.window)
        WindowComponents.active_pages.append(WindowComponents.edit_topic_page)

        frame_width: int = 415
        frame_height: int = 420

        WindowComponents.edit_topic_page.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.edit_topic_page.config(bg = WindowComponents.window_colours[0].colour_code)

        WindowComponents.position_frame(WindowComponents.edit_topic_page, [frame_width, frame_height])
        WindowComponents.make_active(WindowComponents.edit_topic_page)

        # Controls
        WindowComponents.topics_listbox = Listbox(WindowComponents.edit_topic_page, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.topics_listbox.place(x = 25, y = 25, width = 175, height = 225)

        id_sort_topics(CommonData.topic_list)
        for topic in CommonData.topic_list:
            WindowComponents.topics_listbox.insert('end', f"{topic.topic_id} - {topic.topic_name}")

        select_topic: Button = Button(WindowComponents.edit_topic_page, text = "Select Topic", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = TopicControls.select_topic)
        select_topic.place(x = 25, y = 260, width = 175, height = 30)

        revert_topic: Button = Button(WindowComponents.edit_topic_page, text = "Revert Changes", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = TopicControls.revert_topic)
        revert_topic.place(x = 25, y = 295, width = 175, height = 30)

        back_button: Button = Button(WindowComponents.edit_topic_page, text = "Back", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Edit Topics", "Home Page"))
        back_button.place(x = 25, y = 365, width = 85, height = 30)

        centre_window: Button = Button(WindowComponents.edit_topic_page, text = "Center", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowComponents.position_frame, WindowComponents.edit_topic_page, [frame_width, frame_height]))
        centre_window.place(x = 115, y = 365, width = 85, height = 30)

        update_topic: Button = Button(WindowComponents.edit_topic_page, text = "Update Topic", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = TopicControls.update_topic)
        update_topic.place(x = 25, y = 330, width = 175, height = 30)

        create_topic: Button = Button(WindowComponents.edit_topic_page, text = "Create Topic", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = TopicControls.create_topic)
        create_topic.place(x = 215, y = 365, width = 175, height = 30)

        # Right Hand Side
        topic_name_header: Label = Label(WindowComponents.edit_topic_page, text = "Topic Name", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        topic_name_header.place(x = 215, y = 25, width = 175, height = 30)

        WindowComponents.topic_name_entry = Entry(WindowComponents.edit_topic_page, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.topic_name_entry.place(x = 215, y = 60, width = 175, height = 30)

        WindowComponents.topic_back_colour = StringVar()
        WindowComponents.topic_text_colour = StringVar()

        topic_background_header: Label = Label(WindowComponents.edit_topic_page, text = "Background Colour", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        topic_background_header.place(x = 215, y = 105, width = 175, height = 30)

        select_background: ttk.ComboBox = ttk.Combobox(WindowComponents.edit_topic_page, textvariable = WindowComponents.topic_back_colour)
        select_background['values'] = CommonData.colour_names
        select_background['state'] = 'readonly'
        select_background.place(x = 215, y = 140, width = 175, height = 30)

        topic_text_header: Label = Label(WindowComponents.edit_topic_page, text = "Text Colour", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        topic_text_header.place(x = 215, y = 185, width = 175, height = 30)

        select_text: ttk.ComboBox = ttk.Combobox(WindowComponents.edit_topic_page, textvariable = WindowComponents.topic_text_colour)
        select_text['values'] = CommonData.colour_names
        select_text['state'] = 'readonly'
        select_text.place(x = 215, y = 220, width = 175, height = 30)

        WindowComponents.contrast_output = Label(WindowComponents.edit_topic_page, text = "Contrast Ratio: Something", bg = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code, fg = CommonData.get_colour_from_name("White", 0, len(CommonData.colour_list)).colour_code, font = WindowComponents.main_font)
        WindowComponents.contrast_output.place(x = 215, y = 260, width = 175, height = 50)

        update_contrast: Button = Button(WindowComponents.edit_topic_page, text = "Update Contrast Ratio", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(ColourControls.set_contrast_ratio, "Topics", WindowComponents.contrast_output))
        update_contrast.place(x = 215, y = 315, width = 175, height = 45)

    def create_edit_colour_page() -> None:
        WindowComponents.edit_colour_page = Toplevel(WindowComponents.window)
        WindowComponents.active_pages.append(WindowComponents.edit_colour_page)

        frame_width: int = 415
        frame_height: int = 420

        WindowComponents.edit_colour_page.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.edit_colour_page.config(bg = WindowComponents.window_colours[0].colour_code)

        WindowComponents.position_frame(WindowComponents.edit_colour_page, [frame_width, frame_height])
        WindowComponents.make_active(WindowComponents.edit_colour_page)

        # Controls
        WindowComponents.colours_listbox = Listbox(WindowComponents.edit_colour_page, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.colours_listbox.place(x = 25, y = 25, width = 175, height = 260)

        id_sort_colours(CommonData.colour_list)
        for colour in CommonData.colour_list:
            WindowComponents.colours_listbox.insert('end', f"{colour.colour_id} - {colour.colour_name}")

        select_colour: Button = Button(WindowComponents.edit_colour_page, text = "Select Colour", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = ColourControls.select_colour)
        select_colour.place(x = 25, y = 295, width = 175, height = 30)

        revert_colour: Button = Button(WindowComponents.edit_colour_page, text = "Revert Changes", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = ColourControls.revert_colour)
        revert_colour.place(x = 25, y = 330, width = 175, height = 30)

        back_button: Button = Button(WindowComponents.edit_colour_page, text = "Back", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Edit Colours", "Home Page"))
        back_button.place(x = 25, y = 365, width = 85, height = 30)

        centre_window: Button = Button(WindowComponents.edit_colour_page, text = "Center", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowComponents.position_frame, WindowComponents.edit_colour_page, [frame_width, frame_height]))
        centre_window.place(x = 115, y = 365, width = 85, height = 30)

        update_colour: Button = Button(WindowComponents.edit_colour_page, text = "Update Colour", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = ColourControls.update_colour)
        update_colour.place(x = 215, y = 295, width = 175, height = 30)

        create_colour: Button = Button(WindowComponents.edit_colour_page, text = "Create Colour", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = ColourControls.create_colour)
        create_colour.place(x = 215, y = 330, width = 175, height = 30)

        clear_colour: Button = Button(WindowComponents.edit_colour_page, text = "Clear Colour", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = ColourControls.clear_colour)
        clear_colour.place(x = 215, y = 365, width = 175, height = 30)

        # Right Hand Side
        colour_name_header: Label = Label(WindowComponents.edit_colour_page, text = "Colour Name", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        colour_name_header.place(x = 215, y = 25, width = 175, height = 30)

        WindowComponents.colour_name_entry = Entry(WindowComponents.edit_colour_page, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.colour_name_entry.place(x = 215, y = 60, width = 175, height = 30)

        colour_code_header: Label = Label(WindowComponents.edit_colour_page, text = "Colour Code", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        colour_code_header.place(x = 215, y = 105, width = 175, height = 30)

        WindowComponents.colour_code_entry = Entry(WindowComponents.edit_colour_page, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.colour_code_entry.place(x = 215, y = 140, width = 175, height = 30)

        colour_output_border = Label(WindowComponents.edit_colour_page, bg = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code)
        colour_output_border.place(x = 215, y = 185, width = 175, height = 65)

        WindowComponents.colour_output = Label(WindowComponents.edit_colour_page, bg = CommonData.get_colour_from_name("Black", 0, len(CommonData.colour_list)).colour_code)
        WindowComponents.colour_output.place(x = 225, y = 195, width = 155, height = 45)

        set_output_button: Button = Button(WindowComponents.edit_colour_page, text = "View Colour", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = ColourControls.set_colour_output)
        set_output_button.place(x = 215, y = 255, width = 175, height = 30)

    def create_edit_audio_page() -> None:
        WindowComponents.edit_audio_page = Toplevel(WindowComponents.window)
        WindowComponents.active_pages.append(WindowComponents.edit_audio_page)

        frame_width: int = 415
        frame_height: int = 345

        WindowComponents.edit_audio_page.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.edit_audio_page.config(bg = WindowComponents.window_colours[0].colour_code)

        WindowComponents.position_frame(WindowComponents.edit_audio_page, [frame_width, frame_height])
        WindowComponents.make_active(WindowComponents.edit_audio_page)

        # Controls
        WindowComponents.audios_listbox = Listbox(WindowComponents.edit_audio_page, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.audios_listbox.place(x = 25, y = 25, width = 175, height = 185)

        id_sort_audios(CommonData.audio_list)
        for audio in CommonData.audio_list:
            WindowComponents.audios_listbox.insert('end', f"{audio.audio_id} - {audio.audio_name}")

        select_audio: Button = Button(WindowComponents.edit_audio_page, text = "Select Audio", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = AudioControls.select_audio)
        select_audio.place(x = 25, y = 220, width = 175, height = 30)

        revert_audio: Button = Button(WindowComponents.edit_audio_page, text = "Revert Changes", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = AudioControls.revert_audio)
        revert_audio.place(x = 25, y = 255, width = 175, height = 30)

        back_button: Button = Button(WindowComponents.edit_audio_page, text = "Back", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Edit Audios", "Home Page"))
        back_button.place(x = 25, y = 290, width = 85, height = 30)

        centre_window: Button = Button(WindowComponents.edit_audio_page, text = "Center", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowComponents.position_frame, WindowComponents.edit_audio_page, [frame_width, frame_height]))
        centre_window.place(x = 115, y = 290, width = 85, height = 30)

        update_audio: Button = Button(WindowComponents.edit_audio_page, text = "Update Audio", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = AudioControls.update_audio)
        update_audio.place(x = 215, y = 220, width = 175, height = 30)

        create_audio: Button = Button(WindowComponents.edit_audio_page, text = "Create Audio", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = AudioControls.create_audio)
        create_audio.place(x = 215, y = 255, width = 175, height = 30)

        clear_audio: Button = Button(WindowComponents.edit_audio_page, text = "Clear Audio", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = AudioControls.clear_audio)
        clear_audio.place(x = 215, y = 290, width = 175, height = 30)

        # Right Hand Side
        audio_name_header: Label = Label(WindowComponents.edit_audio_page, text = "Audio Name", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        audio_name_header.place(x = 215, y = 25, width = 175, height = 30)

        WindowComponents.audio_name_entry = Entry(WindowComponents.edit_audio_page, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.audio_name_entry.place(x = 215, y = 60, width = 175, height = 30)

        audio_file_header: Label = Label(WindowComponents.edit_audio_page, text = "Audio File", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        audio_file_header.place(x = 215, y = 105, width = 175, height = 30)

        WindowComponents.audio_file_entry = Entry(WindowComponents.edit_audio_page, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.audio_file_entry.place(x = 215, y = 140, width = 175, height = 30)

        preview_audio_button: Button = Button(WindowComponents.edit_audio_page, text = "Preview Audio", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = AudioControls.preview_audio)
        preview_audio_button.place(x = 215, y = 180, width = 175, height = 30)

    def create_view_account_page() -> None:
        WindowComponents.view_account_page = Toplevel(WindowComponents.window)
        WindowComponents.active_pages.append(WindowComponents.view_account_page)

        frame_width: int = 225
        frame_height: int = 185

        WindowComponents.view_account_page.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.view_account_page.config(bg = WindowComponents.window_colours[0].colour_code)

        WindowComponents.position_frame(WindowComponents.view_account_page, [frame_width, frame_height])
        WindowComponents.make_active(WindowComponents.view_account_page)

        login_header: Label = Label(WindowComponents.view_account_page, text = WindowComponents.active_user.username, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        login_header.place(x = 25, y = 25, width = 175, height = 30)

        edit_account_button: Button = Button(WindowComponents.view_account_page, text = "Edit Account", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "View Account", "Edit Account"))
        edit_account_button.place(x = 25, y = 60, width = 175, height = 30)

        view_past_quizzes_button: Button = Button(WindowComponents.view_account_page, text = "View Past Quizzes", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "View Account", "View Past Quizzes"))
        view_past_quizzes_button.place(x = 25, y = 95, width = 175, height = 30)

        #view_leaderboard_button: Button = Button(WindowComponents.view_account_page, text = "View Leaderboard", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "View Account", "View Leaderboard"))
        #view_leaderboard_button.place(x = 25, y = 160, width = 175, height = 30)

        back_button: Button = Button(WindowComponents.view_account_page, text = "Back", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "View Account", "Home Page"))
        back_button.place(x = 25, y = 130, width = 85, height = 30)

        centre_window: Button = Button(WindowComponents.view_account_page, text = "Center", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowComponents.position_frame, WindowComponents.view_account_page, [frame_width, frame_height]))
        centre_window.place(x = 115, y = 130, width = 85, height = 30)

    def create_edit_account_page() -> None:
        WindowComponents.edit_account_page = Toplevel(WindowComponents.window)
        WindowComponents.active_pages.append(WindowComponents.edit_account_page)

        frame_width: int = 445
        frame_height: int = 380

        WindowComponents.edit_account_page.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.edit_account_page.config(bg = WindowComponents.window_colours[0].colour_code)

        WindowComponents.position_frame(WindowComponents.edit_account_page, [frame_width, frame_height])
        WindowComponents.make_active(WindowComponents.edit_account_page)

        login_header: Label = Label(WindowComponents.edit_account_page, text = "Update Account Page", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        login_header.place(x = 25, y = 25, width = 175, height = 30)

        username_header: Label = Label(WindowComponents.edit_account_page, text = "Username", bg = WindowComponents.window_colours[0].colour_code, fg = WindowComponents.window_colours[1].colour_code, font = WindowComponents.main_font)
        username_header.place(x = 25, y = 70, width = 175, height = 20)

        WindowComponents.update_username_entry = Entry(WindowComponents.edit_account_page, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.update_username_entry.place(x = 25, y = 95, width = 175, height = 30)

        password_header: Label = Label(WindowComponents.edit_account_page, text = "Password", bg = WindowComponents.window_colours[0].colour_code, fg = WindowComponents.window_colours[1].colour_code, font = WindowComponents.main_font)
        password_header.place(x = 25, y = 140, width = 175, height = 20)

        WindowComponents.update_password_entry = Entry(WindowComponents.edit_account_page, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.update_password_entry.place(x = 25, y = 165, width = 175, height = 30)


        # Colour stuffs

        colours_border: Label = Label(WindowComponents.edit_account_page, bg = "#000000")
        colours_border.place(x = 225, y = 25, width = 195, height = 330)

        WindowComponents.ua_background_display = Label(WindowComponents.edit_account_page, bg = WindowComponents.window_colours[0].colour_code)
        WindowComponents.ua_background_display.place(x = 240, y = 40, width = 165, height = 300)

        WindowComponents.ua_window_display = Label(WindowComponents.edit_account_page, text = "Window Colours", bg = WindowComponents.window_colours[0].colour_code, fg = WindowComponents.window_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.ua_window_display.place(x = 255, y = 55, width = 135, height = 45)

        WindowComponents.ua_label_display = Label(WindowComponents.edit_account_page, text = "Label Colours", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.ua_label_display.place(x = 255, y = 115, width = 135, height = 60)

        WindowComponents.ua_button_display = Button(WindowComponents.edit_account_page, text = "Button Colours", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.ua_button_display.place(x = 255, y = 190, width = 135, height = 60)

        WindowComponents.ua_entry_display = Label(WindowComponents.edit_account_page, text = "Entry Colours", bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.ua_entry_display.place(x = 255, y = 265, width = 135, height = 60)


        # Insert User Data

        WindowComponents.update_username_entry.insert(0, WindowComponents.active_user.username)
        WindowComponents.update_password_entry.insert(0, decrypyt_password(WindowComponents.active_user.password, WindowComponents.active_user.password_shift))


        # Control Buttons

        choose_colours_button: Button = Button(WindowComponents.edit_account_page, text = "Choose Colours", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.open_colour_selector, "Update User Colours"))
        choose_colours_button.place(x = 25, y = 220, width = 175, height = 30)

        create_account_button: Button = Button(WindowComponents.edit_account_page, text = "Update Account", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowDesign.update_account)
        create_account_button.place(x = 25, y = 255, width = 175, height = 30)

        revert_changes: Button = Button(WindowComponents.edit_account_page, text = "Revert Changes", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowControls.revert_account)
        revert_changes.place(x = 25, y = 290, width = 175, height = 30)

        back_button: Button = Button(WindowComponents.edit_account_page, text = "Back", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Edit Account", "View Account"))
        back_button.place(x = 25, y = 325, width = 85, height = 30)

        centre_window: Button = Button(WindowComponents.edit_account_page, text = "Center", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowComponents.position_frame, WindowComponents.edit_account_page, [frame_width, frame_height]))
        centre_window.place(x = 115, y = 325, width = 85, height = 30)

    def create_view_past_quizzes_page() -> None: messagebox.showinfo("Page Doesn't Exist", "This Page Doesn't Exist Yet")
    def create_view_leaderboard_page() -> None: messagebox.showinfo("Page Doesn't Exist", "This Page Doesn't Exist Yet")


    # Question Editor Frames

    def create_edit_question_page_template() -> Toplevel:
        return_frame: Toplevel = Toplevel(WindowComponents.window)
        return_frame.withdraw()

        frame_width: int = 1000
        frame_height: int = 600

        return_frame.geometry(f"{frame_width}x{frame_height}")
        return_frame.config(bg = WindowComponents.window_colours[0].colour_code)

        WindowComponents.position_frame(return_frame, [frame_width, frame_height])

        # Question Text Entry
        question_entry_header = Label(return_frame, text = "Enter Question Text", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        question_entry_header.place(x = 25, y = 25, width = 355, height = 30)

        WindowComponents.question_text_input = Text(return_frame, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.question_text_input.place(x = 25, y = 60, width = 355, height = 100)

        # Details Header
        question_details_header = Label(return_frame, text = "Question Details", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        question_details_header.place(x = 755, y = 25, width = 175, height = 30)

        # Select Question Topic
        WindowComponents.topic_selector = Listbox(return_frame, selectmode = 'multiple', exportselection = False, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.topic_selector.place(x = 755, y = 60, width = 175, height = 205)

        id_sort_topics(CommonData.topic_list)
        for topic in CommonData.topic_list:
            WindowComponents.topic_selector.insert('end', f"{topic.topic_id} - {topic.topic_name}")

        # Question Difficulty
        difficulties: list[str] = WindowComponents.question_difficulties.copy()
        difficulties.remove("All")
        # print(difficulties)

        WindowComponents.difficulty_selector = ttk.Combobox(return_frame)
        WindowComponents.difficulty_selector['values'] = ["Question Difficulty"] + difficulties
        WindowComponents.difficulty_selector['state'] = 'readonly'
        WindowComponents.difficulty_selector.place(x = 755, y = 270, width = 175, height = 30)
        WindowComponents.chosen_difficulty = StringVar()
        WindowComponents.difficulty_selector.configure(textvariable = WindowComponents.chosen_difficulty)
        WindowComponents.chosen_difficulty.set("Question Difficulty")

        # Question Score
        WindowComponents.question_score_selector = ttk.Combobox(return_frame)
        WindowComponents.question_score_selector['values'] = ["Question Score"] + list(range(1, 5))
        WindowComponents.question_score_selector['state'] = 'readonly'
        WindowComponents.question_score_selector.place(x = 755, y = 305, width = 175, height = 30)
        WindowComponents.chosen_question_score = StringVar()
        WindowComponents.question_score_selector.configure(textvariable = WindowComponents.chosen_question_score)
        WindowComponents.chosen_question_score.set("Question Score")

        # Correct Answer Audio
        WindowComponents.correct_audio_selector = ttk.Combobox(return_frame)
        WindowComponents.correct_audio_selector['values'] = ["Correct Audio"] + CommonData.audio_names
        WindowComponents.correct_audio_selector['state'] = 'readonly'
        WindowComponents.correct_audio_selector.place(x = 755, y = 340, width = 175, height = 30)
        WindowComponents.chosen_correct_audio = StringVar()
        WindowComponents.correct_audio_selector.configure(textvariable = WindowComponents.chosen_correct_audio)
        WindowComponents.chosen_correct_audio.set("Correct Audio")

        # Incorrect Answer Audio
        WindowComponents.incorrect_audio_selector = ttk.Combobox(return_frame)
        WindowComponents.incorrect_audio_selector['values'] = ["Incorrect Audio"] + CommonData.audio_names
        WindowComponents.incorrect_audio_selector['state'] = 'readonly'
        WindowComponents.incorrect_audio_selector.place(x = 755, y = 375, width = 175, height = 30)
        WindowComponents.chosen_incorrect_audio = StringVar()
        WindowComponents.incorrect_audio_selector.configure(textvariable = WindowComponents.chosen_incorrect_audio)
        WindowComponents.chosen_incorrect_audio.set("Incorrect Audio")

        # Hint Header
        hint_header: Label = Label(return_frame, text = "Hints", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        hint_header.place(x = 385, y = 25, width = 355, height = 30)

        # Reset Toggles
        WindowComponents.add_text_hint = True
        WindowComponents.is_image_question = False

        # Text Hint Button
        WindowComponents.text_hint_button = Button(return_frame, text = f"Add Text Hint: {WindowComponents.add_text_hint}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowControls.toggle_text_hint)
        WindowComponents.text_hint_button.place(x = 385, y = 60, width = 175, height = 30)

        # 50/50 Hint Button
        WindowComponents.relevant_hint_button = Button(return_frame, bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.relevant_hint_button.place(x = 385, y = 95, width = 175, height = 30)

        # 50/50 Hint Button
        WindowComponents.image_question_button = Button(return_frame, text = f"Image Question: {WindowComponents.is_image_question}", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowControls.toggle_image_question)
        WindowComponents.image_question_button.place(x = 385, y = 130, width = 175, height = 30)

        # Text Hint Header
        WindowComponents.text_hint_header = Label(return_frame, text = "Enter Text Hint Text", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.text_hint_header.place(x = 565, y = 60, width = 175, height = 30)

        # Text Hint Entry
        WindowComponents.text_hint_entry = Text(return_frame, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.text_hint_entry.place(x = 565, y = 95, width = 175, height = 65)

        # Image File Entry Header
        image_file_entry_header: Label = Label(return_frame, text = "Enter Image File Location", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        image_file_entry_header.place(x = 25, y = 165, width = 175, height = 30)

        # Image File Entry
        WindowComponents.image_file_entry = Entry(return_frame, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.image_file_entry.place(x = 205, y = 165, width = 355, height = 30)

        # View Image Preview
        WindowComponents.view_image_preview = Button(return_frame, text = "View Image Preview", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = WindowControls.view_image_preview)
        WindowComponents.view_image_preview.place(x = 565, y = 165, width = 175, height = 30)

        # Fun Fact Header
        fun_fact_header: Label = Label(return_frame, text = "Enter Fun Fact", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        fun_fact_header.place(x = 25, y = 200, width = 175, height = 30)

        # Fun Fact Entry
        WindowComponents.fun_fact_entry = Entry(return_frame, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.fun_fact_entry.place(x = 205, y = 200, width = 535, height = 30)

        # 50/50 Hint (Remove on Non-Closed Questions / replace with 'Place 1 Item' in Order Questions?)

        # View Question Preview
        WindowComponents.view_preview = Button(return_frame, text = "View Question Preview", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.view_preview.place(x = 25, y = 510, width = 355, height = 30)

        # Create Question
        WindowComponents.create_question = Button(return_frame, text = "Create Question", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.create_question.place(x = 385, y = 510, width = 355, height = 30)

        # Back Button
        WindowComponents.back_button = Button(return_frame, text = "Back", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowDesign.page_controller, "Edit Question", "Edit Question Selector"))
        WindowComponents.back_button.place(x = 25, y = 545, width = 235, height = 30)

        # Center Window
        WindowComponents.centre_window = Button(return_frame, text = "Center", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font, command = functools.partial(WindowComponents.position_frame, return_frame, [frame_width, frame_height]))
        WindowComponents.centre_window.place(x = 265, y = 545, width = 235, height = 30)

        # Clear Question Details
        WindowComponents.clear_window = Button(return_frame, text = "Clear", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.clear_window.place(x = 505, y = 545, width = 235, height = 30)

        return return_frame

    def create_edit_closed_question_page() -> None:
        WindowComponents.edit_question_page = WindowDesign.create_edit_question_page_template()

        x_start: int = 25

        WindowComponents.answers.clear()
        for i in range(4): WindowComponents.answers.append(AnswerCreator(WindowComponents.edit_question_page, i + 1, x_start + (i * (175 + 5))))
        
        # Relocate Sidebar Controls
        WindowComponents.topic_selector.place(height = 445)
        WindowComponents.difficulty_selector.place(y = 510)
        WindowComponents.question_score_selector.place(y = 545)
        WindowComponents.correct_audio_selector.place(y = 580)
        WindowComponents.incorrect_audio_selector.place(y = 615)
        
        # Relocate Bottom Control Buttons
        WindowComponents.view_preview.place(y = 580)
        WindowComponents.create_question.place(y = 580)
        WindowComponents.back_button.place(y = 615)
        WindowComponents.centre_window.place(y = 615)
        WindowComponents.clear_window.place(y = 615)

        # Reset Toggle
        WindowComponents.add_50_50_hint = False

        # Set Button Commands
        WindowComponents.relevant_hint_button.configure(text = f"Add 50/50 Hint: {WindowComponents.add_50_50_hint}", command = WindowControls.toggle_50_50_hint)
        WindowComponents.view_preview.configure(command = functools.partial(WindowDesign.view_question_preview, "Closed"))
        WindowComponents.clear_window.configure(command = functools.partial(WindowControls.clear_edit_questions_page, "Closed"))

        # Set Frame Geometry + Center
        frame_width: int = 955
        frame_height: int = 670

        WindowComponents.edit_question_page.geometry(f"{frame_width}x{frame_height}")

        WindowComponents.position_frame(WindowComponents.edit_question_page, [frame_width, frame_height])
        WindowComponents.centre_window.configure(command = functools.partial(WindowComponents.position_frame, WindowComponents.edit_question_page, [frame_width, frame_height]))

        WindowComponents.create_question.configure(command = QuestionController.create_closed_question)

        WindowComponents.edit_question_page.update()
        WindowComponents.edit_question_page.deiconify()

        WindowComponents.make_active(WindowComponents.edit_question_page)

    def create_edit_open_question_page() -> None:
        WindowComponents.edit_question_page = WindowDesign.create_edit_question_page_template()

        # Reset Toggle
        WindowComponents.add_provide_word_hint = False

        # Set Button Commands
        WindowComponents.relevant_hint_button.configure(text = f"Add Provide Word: {WindowComponents.add_provide_word_hint}", command = WindowControls.toggle_provide_word_hint)
        WindowComponents.view_preview.configure(command = functools.partial(WindowDesign.view_question_preview, "Open"))
        WindowComponents.clear_window.configure(command = functools.partial(WindowControls.clear_edit_questions_page, "Open"))

        # Answer Details Entry
        acceptable_header: Label = Label(WindowComponents.edit_question_page, text = "Enter Required Words", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        acceptable_header.place(x = 25, y = 235, width = 175, height = 30)

        WindowComponents.open_answer_required = Entry(WindowComponents.edit_question_page, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.open_answer_required.place(x = 205, y = 235, width = 535, height = 30)
        
        rejectable_header: Label = Label(WindowComponents.edit_question_page, text = "Enter Acceptable Words", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        rejectable_header.place(x = 25, y = 270, width = 175, height = 30)

        WindowComponents.open_answer_acceptable = Entry(WindowComponents.edit_question_page, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.open_answer_acceptable.place(x = 205, y = 270, width = 535, height = 30)
        
        # Relocate Sidebar Controls
        WindowComponents.topic_selector.place(height = 170)
        WindowComponents.difficulty_selector.place(y = 235)
        WindowComponents.question_score_selector.place(y = 270)
        WindowComponents.correct_audio_selector.place(y = 305)
        WindowComponents.incorrect_audio_selector.place(y = 340)
        
        # Relocate Bottom Control Buttons
        WindowComponents.view_preview.place(y = 305)
        WindowComponents.create_question.place(y = 305)
        WindowComponents.back_button.place(y = 340)
        WindowComponents.centre_window.place(y = 340)
        WindowComponents.clear_window.place(y = 340)

        # Hint Reshuffling
        WindowComponents.text_hint_header.destroy()
        WindowComponents.text_hint_entry.place(x = 385)
        
        WindowComponents.relevant_hint_button.place(x = 565, y = 60)
        WindowComponents.image_question_button.place(x = 565)

        WindowComponents.relevant_hint_entry = Entry(WindowComponents.edit_question_page, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.relevant_hint_entry.place(x = 565, y = 95, width = 175, height = 30)

        # Set Frame Geometry + Center
        frame_width: int = 955
        frame_height: int = 395

        WindowComponents.edit_question_page.geometry(f"{frame_width}x{frame_height}")

        WindowComponents.position_frame(WindowComponents.edit_question_page, [frame_width, frame_height])
        WindowComponents.centre_window.configure(command = functools.partial(WindowComponents.position_frame, WindowComponents.edit_question_page, [frame_width, frame_height]))

        WindowComponents.create_question.configure(command = QuestionController.create_open_question)

        WindowComponents.edit_question_page.update()
        WindowComponents.edit_question_page.deiconify()

        WindowComponents.make_active(WindowComponents.edit_question_page)

    def create_edit_order_question_page() -> None:
        WindowComponents.edit_question_page = WindowDesign.create_edit_question_page_template()
        
        WindowComponents.edit_question_page.update()
        WindowComponents.edit_question_page.deiconify()

        WindowComponents.make_active(WindowComponents.edit_question_page)


    # Insert Question Data (Editing)

    def insert_common_items() -> None:
        # Insert Question Text
        WindowComponents.question_text_input.delete("1.0", END)
        WindowComponents.question_text_input.insert("1.0", WindowComponents.current_edit_question.question_text)

        # Insert Question Hint
        WindowComponents.text_hint_entry.delete("1.0", END)
        if WindowComponents.current_edit_question.add_text_hint: WindowComponents.text_hint_entry.insert("1.0", WindowComponents.current_edit_question.text_hint)

        # Insert Image File (If Applicable)
        WindowComponents.image_file_entry.delete(0, len(WindowComponents.image_file_entry.get()))
        if WindowComponents.current_edit_question.is_image_question: WindowComponents.image_file_entry.insert(0, WindowComponents.current_edit_question.image_file)

        # Insert Fun Fact
        WindowComponents.fun_fact_entry.delete(0, len(WindowComponents.fun_fact_entry.get()))
        WindowComponents.fun_fact_entry.insert(0, WindowComponents.current_edit_question.fun_fact)

        # Set States of Hint Buttons
        WindowComponents.add_text_hint = WindowComponents.current_edit_question.add_text_hint
        WindowComponents.is_image_question = WindowComponents.current_edit_question.is_image_question

        WindowComponents.text_hint_button.configure(text = f"Add Text Hint: {WindowComponents.current_edit_question.add_text_hint}")
        WindowComponents.image_question_button.configure(text = f"Image Question: {WindowComponents.current_edit_question.is_image_question}")

        if not WindowComponents.add_text_hint: WindowComponents.text_hint_button.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
        if WindowComponents.is_image_question: WindowComponents.image_question_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

        # Select Topics (Needs Work)
        # for topic in WindowComponents.current_edit_question.question_topics:
        #     print(int(topic.replace("T","")) - 1)
        #     WindowComponents.topic_selector.activate(int(topic.replace("T","")) - 1)
            
        # Insert Difficulty, Score + Audios
        WindowComponents.difficulty_selector.set(WindowComponents.current_edit_question.question_difficulty)
        WindowComponents.question_score_selector.set(int(WindowComponents.current_edit_question.question_points))
        WindowComponents.correct_audio_selector.set(CommonData.get_audio_from_id(WindowComponents.current_edit_question.correct_audio, 0, len(CommonData.audio_list)).audio_name)
        WindowComponents.incorrect_audio_selector.set(CommonData.get_audio_from_id(WindowComponents.current_edit_question.incorrect_audio, 0, len(CommonData.audio_list)).audio_name)

        # Set 'Create Question' to 'Update Question'
        WindowComponents.create_question.configure(text = "Update Question", command = QuestionController.update_closed_question)

    def edit_closed_question() -> None:
        WindowDesign.create_edit_closed_question_page()
        WindowDesign.insert_common_items()

        # Set States of Hint Buttons
        WindowComponents.add_50_50_hint = WindowComponents.current_edit_question.add_50_50_hint
        WindowComponents.relevant_hint_button.configure(text = f"Add 50/50 Hint: {WindowComponents.current_edit_question.add_50_50_hint}")
        if WindowComponents.add_50_50_hint: WindowComponents.relevant_hint_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

        answer: Answer
        answer_region: AnswerCreator

        for answer_number in range(len(WindowComponents.current_edit_question.answers)):
            answer = WindowComponents.current_edit_question.answers[answer_number]
            answer_region = WindowComponents.answers[answer_number]

            # answer.display_answer()

            # Insert Answer Texts
            answer_region.answer_entry.insert("1.0", answer.answer_text)

            # Set Answer Colours
            answer_region.background.set(CommonData.get_colour_from_id(answer.answer_back_colour, 0, len(CommonData.colour_list)).colour_name)
            answer_region.foreground.set(CommonData.get_colour_from_id(answer.answer_text_colour, 0, len(CommonData.colour_list)).colour_name)

            # Set Correct Answer
            answer_region.is_correct_answer.configure(text = f"Correct Answer: {answer.correct_answer}")
            if answer.correct_answer: answer_region.is_correct_answer.configure(bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)
            else: answer_region.is_correct_answer.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)

            # answer_number += 1

        # Set Unincluded Answers (If Applicable)
        if answer_number < 3:
            while answer_number < 4:
                WindowComponents.answers[answer_number].include_answer = False
                WindowComponents.answers[answer_number].include_button.configure(text = f"Include Answer: False", bg = WindowComponents.button_colours[1].colour_code, fg = WindowComponents.button_colours[0].colour_code)

                answer_number += 1

    def edit_open_question() -> None:
        WindowDesign.create_edit_open_question_page()
        WindowDesign.insert_common_items()

        # Set States of Hint Buttons
        WindowComponents.add_provide_word_hint = WindowComponents.current_edit_question.provide_word_hint
        WindowComponents.relevant_hint_button.configure(text = f"Add Provide Word: {WindowComponents.current_edit_question.provide_word_hint}")

        if WindowComponents.add_provide_word_hint:
            WindowComponents.relevant_hint_button.configure(bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code)
            WindowComponents.relevant_hint_entry.delete(0, len(WindowComponents.relevant_hint_entry.get()))
            WindowComponents.relevant_hint_entry.insert(0, WindowComponents.current_edit_question.provided_word)

        # Insert Answers
        WindowComponents.open_answer_required.delete(0, END)
        WindowComponents.open_answer_acceptable.delete(0, END)

        required_words: str = WindowComponents.current_edit_question.required_words[0]
        acceptable_words: str = WindowComponents.current_edit_question.acceptable_words[0]

        for i in range(1, len(WindowComponents.current_edit_question.required_words)): required_words += f" {WindowComponents.current_edit_question.required_words[i]}"
        for i in range(1, len(WindowComponents.current_edit_question.acceptable_words)): acceptable_words += f" {WindowComponents.current_edit_question.acceptable_words[i]}"

        WindowComponents.open_answer_required.insert(0, required_words)
        WindowComponents.open_answer_acceptable.insert(0, acceptable_words)

    def edit_order_question() -> None: pass


    # Question Editor Functions

    def view_question_preview(question_type: str) -> None:
        if WindowComponents.question_view != None and WindowComponents.question_view.winfo_exists(): WindowComponents.question_view.destroy()

        match question_type:
            case "Closed":
                if not QuestionController.valid_closed_question(): return 0
                QuestionDesign.create_closed_question_view() # WindowComponents.is_image_question)
                WindowControls.view_closed_preview(QuestionController.create_partial_closed_dict())
            case "Open":
                if not QuestionController.valid_open_question(): return 0
                QuestionDesign.create_open_question_view() # WindowComponents.is_image_question)
                WindowControls.view_open_preview(QuestionController.create_partial_open_dict())
            case "Order": messagebox.showerror("Page Non-Existent", "Question Page Doesn't Exist")


    #   Login Functions

    def logout() -> None:
        WindowComponents.active_user = None
        destroy_all_pages(WindowComponents.active_pages)
        WindowDesign.create_login_page()

    def attempt_login() -> None:
        entered_username = WindowComponents.username_entry.get()
        entered_password = WindowComponents.password_entry.get()

        if entered_username == "" or entered_password == "":
            messagebox.showinfo("Login Error", "Please Enter User Details")
            WindowComponents.password_entry.delete(0, len(entered_password))
        elif login(entered_username, entered_password):
            WindowComponents.login_page.destroy()
            WindowComponents.active_user = CommonData.get_account_from_name(entered_username, 0, len(CommonData.players))
            WindowDesign.create_home_page()
        else:
            messagebox.showinfo("Login Error", "Invalid User Details")
            WindowComponents.password_entry.delete(0, len(entered_password))

    def login_as_guest() -> None:
        print("Login as Guest")

        # Needs to Generate Guest ID (Guest#XXXX)
        # Creates Guest User Account, cant be re-accessed after user logs out

    def create_account() -> None:
        username: str = WindowComponents.create_username_entry.get()
        password: str = WindowComponents.create_password_entry.get()

        if not unique_username(username, None):
            messagebox.showerror("Account Creation Error - Username", "Invalid Username, Username already taken")
            return 0
        if not valid_password(password):
            messagebox.showerror("Account Creation Error - Password", "Invalid Password, Either too short or uses invalid characters")
            return 0
        if not ColourControls.valid_colours():
            messagebox.showerror("Account Creation Error - Colours", "Invalid Colours, Contrast Too Low")
            return 0

        user_data: dict = WindowControls.jsonify_user_data()

        new_user: Player = Player("Player", user_data)
        write_user_file(new_user)

        WindowComponents.active_user = new_user

        WindowComponents.choose_colours.destroy()
        WindowComponents.create_account_page.destroy()

        messagebox.showinfo("Account Creation Success", "Account Successfully Created\nPress OK to Continue to Home Page")
        WindowDesign.create_home_page()

    def update_account() -> None:
        # Some form of 'This will alter your settings, and can't be undone, are you sure you want to continue?' warning needed here probably

        username: str = WindowComponents.update_username_entry.get()
        password: str = WindowComponents.update_password_entry.get()

        WindowComponents.chosen_window_back = CommonData.get_colour_from_name(WindowComponents.window_back.get(), 0, len(CommonData.colour_list)); WindowComponents.chosen_window_text = CommonData.get_colour_from_name(WindowComponents.window_text.get(), 0, len(CommonData.colour_list))
        WindowComponents.chosen_button_back = CommonData.get_colour_from_name(WindowComponents.button_back.get(), 0, len(CommonData.colour_list)); WindowComponents.chosen_button_text = CommonData.get_colour_from_name(WindowComponents.button_text.get(), 0, len(CommonData.colour_list))
        WindowComponents.chosen_label_back = CommonData.get_colour_from_name(WindowComponents.label_back.get(), 0, len(CommonData.colour_list)); WindowComponents.chosen_label_text = CommonData.get_colour_from_name(WindowComponents.label_text.get(), 0, len(CommonData.colour_list))
        WindowComponents.chosen_entry_back = CommonData.get_colour_from_name(WindowComponents.entry_back.get(), 0, len(CommonData.colour_list)); WindowComponents.chosen_entry_text = CommonData.get_colour_from_name(WindowComponents.entry_text.get(), 0, len(CommonData.colour_list))

        valid_username: bool = unique_username(username, WindowComponents.active_user.username)
        _valid_password: bool = valid_password(password)
        valid_colours: bool = ColourControls.valid_colours()

        if not valid_username:
            messagebox.showerror("Account Update Error - Username", "Invalid Username, Username already taken")
            return 0
        if not _valid_password:
            messagebox.showerror("Account Update Error - Password", "Invalid Password, Either too short or uses invalid characters")
            return 0
        if not valid_colours:
            messagebox.showerror("Account Update Error - Colours", "Invalid Colours, Contrast Too Low")
            return 0

        [encrypted_password, shift_key] = encrypt_password(password)

        WindowComponents.active_user.username = username
        WindowComponents.active_user.password = encrypted_password
        WindowComponents.active_user.password_shift = shift_key

        WindowComponents.active_user.window_colours = [CommonData.get_colour_from_name(WindowComponents.window_back.get(), 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_name(WindowComponents.window_text.get(), 0, len(CommonData.colour_list)).colour_id]
        WindowComponents.active_user.button_colours = [CommonData.get_colour_from_name(WindowComponents.button_back.get(), 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_name(WindowComponents.button_text.get(), 0, len(CommonData.colour_list)).colour_id]
        WindowComponents.active_user.label_colours = [CommonData.get_colour_from_name(WindowComponents.label_back.get(), 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_name(WindowComponents.label_text.get(), 0, len(CommonData.colour_list)).colour_id]
        WindowComponents.active_user.entry_colours = [CommonData.get_colour_from_name(WindowComponents.entry_back.get(), 0, len(CommonData.colour_list)).colour_id, CommonData.get_colour_from_name(WindowComponents.entry_text.get(), 0, len(CommonData.colour_list)).colour_id]

        ColourControls.set_user_colours()

        messagebox.showinfo("Account Update Success", "Account Successfully Updates\nPress OK to Continue")

        write_user_file(WindowComponents.active_user)
        WindowComponents.edit_account_page.destroy()
        WindowDesign.create_edit_account_page()

    #  Open Edit Question

    def open_edit_question() -> None:
        if len(WindowComponents.question_list.curselection()) == 0:
            messagebox.showerror("No Question Selected", "Please Select a Question to Edit")
            return 0

        match WindowComponents.chosen_question_type.get():
            case "Question Type": WindowComponents.current_edit_question = CommonData.get_question(WindowComponents.question_keys[WindowComponents.question_list.curselection()[0]])# , 0, len(CommonData.discarded_questions))
            case "All": WindowComponents.current_edit_question = CommonData.get_question(WindowComponents.question_keys[WindowComponents.question_list.curselection()[0]])# , 0, len(CommonData.discarded_questions))
            case "Usable": WindowComponents.current_edit_question = CommonData.get_usable_question(WindowComponents.question_keys[WindowComponents.question_list.curselection()[0]], 0, len(CommonData.usable_questions))
            case "Discarded": WindowComponents.current_edit_question = CommonData.get_discarded_question(WindowComponents.question_keys[WindowComponents.question_list.curselection()[0]], 0, len(CommonData.discarded_questions))

        WindowDesign.page_controller("Edit Question Selector", "Edit Question", True)

    # Flow Controls

    def open_colour_selector(selector_type: str) -> None:
        if WindowComponents.choose_colours == None or not WindowComponents.choose_colours.winfo_exists():
            WindowDesign.create_choose_colours_page(selector_type)
        else:
            WindowComponents.choose_colours.update()
            WindowComponents.choose_colours.deiconify()

    def page_controller(from_frame: str, to_frame: str, do_hide: bool = False) -> None:
        incomplete: list[str] = ["View Past Quizzes", "View Leaderboard", "Create Order Question"]

        if to_frame in incomplete:
            messagebox.showinfo("Page Doesn't Exist", "This Page Can't Be Displayed As It Doesn't Exist")
            return 0

        # Hide From Frame
        match from_frame:
            case "Login Page": WindowComponents.login_page.destroy() 
            case "Create Account": WindowComponents.create_account_page.destroy()
            case "Home Page": WindowComponents.home_page.destroy()
            case "Setup Quiz": WindowComponents.quiz_setup_page.destroy()
            case "Edit Question Selector":
                if not do_hide: WindowComponents.edit_question_select_page.destroy()
                else: WindowComponents.edit_question_select_page.withdraw()
            case "Edit Question":
                if WindowComponents.question_view != None and WindowComponents.question_view.winfo_exists(): WindowComponents.question_view.destroy()
                if WindowComponents.image_preview_frame != None and WindowComponents.image_preview_frame.winfo_exists(): WindowComponents.image_preview_frame.destroy()
                WindowComponents.edit_question_page.destroy()
            case "Create Question":
                if WindowComponents.question_view != None and WindowComponents.question_view.winfo_exists(): WindowComponents.question_view.destroy()
                if WindowComponents.image_preview_frame != None and WindowComponents.image_preview_frame.winfo_exists(): WindowComponents.image_preview_frame.destroy()
                WindowComponents.edit_question_page.destroy()
            case "Edit Topics": WindowComponents.edit_topic_page.destroy()
            case "Edit Colours": WindowComponents.edit_colour_page.destroy()
            case "Edit Audios": WindowComponents.edit_audio_page.destroy()
            case "View Account": WindowComponents.view_account_page.destroy()
            case "Edit Account": WindowComponents.edit_account_page.destroy()
            case "View Past Quizzes": pass
            case "View Leaderboard": pass

        # Deiconify To Frame
        match to_frame:
            case "Login Page": WindowDesign.create_login_page()
            case "Create Account": WindowDesign.create_create_account_page()
            case "Home Page": WindowDesign.create_home_page()
            case "Setup Quiz": WindowDesign.create_quiz_setup_page()
            case "Edit Question Selector":
                WindowComponents.current_edit_question = None
                if WindowComponents.edit_question_select_page == None or not WindowComponents.edit_question_select_page.winfo_exists(): WindowDesign.create_edit_question_selector_page()
                else:
                    WindowComponents.edit_question_select_page.update()
                    WindowComponents.edit_question_select_page.deiconify()
            case "Edit Question":
                match WindowComponents.current_edit_question.question_type:
                    case "Closed": WindowDesign.edit_closed_question()
                    case "Open": WindowDesign.edit_open_question()
                    case "Order": WindowDesign.edit_order_question()
            case "Create Open Question": WindowDesign.create_edit_open_question_page()
            case "Create Closed Question": WindowDesign.create_edit_closed_question_page()
            case "Create Order Question": WindowDesign.create_edit_order_question_page()
            case "Edit Topics":
                WindowComponents.current_edit_topic = None
                WindowDesign.create_edit_topic_page()
            case "Edit Colours":
                WindowComponents.current_edit_colour = None
                WindowDesign.create_edit_colour_page()
            case "Edit Audios":
                WindowComponents.current_edit_audio = None
                WindowDesign.create_edit_audio_page()
            case "View Account":WindowDesign.create_view_account_page()
            case "Edit Account": WindowDesign.create_edit_account_page()
            case "View Past Quizzes": pass
            case "View Leaderboard": pass
