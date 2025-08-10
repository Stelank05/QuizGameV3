from tkinter import *

from quiz.quiz import Quiz

from window.window_components import WindowComponents
# from window.window_controls import WindowControls

class QuestionDesign:
    # Create Question View Frames
    
    def create_question_view_template() -> Toplevel:
        return_frame: Toplevel = Toplevel(WindowComponents.window)
        return_frame.withdraw()

        frame_width: int = 1000
        frame_height: int = 600

        return_frame.geometry(f"{frame_width}x{frame_height}")
        return_frame.config(bg = WindowComponents.window_colours[0].colour_code)

        WindowComponents.position_frame(return_frame, [frame_width, frame_height])

        # Question Number
        WindowComponents.question_number_output = Label(return_frame, text = "Question Number: N/A", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.question_number_output.place(x = 25, y = 25, width = 175, height = 30)

        # Current Score
        WindowComponents.current_score_output = Label(return_frame, text = "Current Score: N/A", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.current_score_output.place(x = 285, y = 25, width = 175, height = 30)

        # Question Difficulty
        WindowComponents.question_difficulty_output = Label(return_frame, text = "Question Difficulty: N/A", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.question_difficulty_output.place(x = 25, y = 60, width = 175, height = 30)

        WindowComponents.filler_label = Label(return_frame, bg = WindowComponents.label_colours[0].colour_code)
        WindowComponents.filler_label.place(x = 200, y = 60, width = 85, height = 30)

        # Question Score
        WindowComponents.question_score_output = Label(return_frame, text = "Question Score: N/A", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.question_score_output.place(x = 285, y = 60, width = 175, height = 30)

        # Question Text
        WindowComponents.question_text_output = Label(return_frame, text = "Question Text: N/A", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.question_text_output.place(x = 25, y = 90, width = 435, height = 65)

        WindowComponents.text_hint_output = Label(return_frame, text = "Hint Text: N/A", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.text_hint_output.place(x = 25, y = 160, width = 435, height = 30)

        # Topics
        WindowComponents.topics_shroud = Label(return_frame, bg = WindowComponents.window_colours[1].colour_code, fg = WindowComponents.window_colours[0].colour_code)
        WindowComponents.topics_shroud.place(x = 475, y = 25, width = 195, height = 300) # (5 * 30) + (4 * 5) + (10 * 2) = 150 + 20 + 20 = 150 + 40 = 190

        WindowComponents.topics_shroud_header = Label(return_frame, text = "Question Topics", bg = WindowComponents.window_colours[0].colour_code, fg = WindowComponents.window_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.topics_shroud_header.place(x = 485, y = 35, width = 175, height = 30)

        # Hints Available
        WindowComponents.view_text_hint_button = Button(return_frame, text = "View Text Hint", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.view_text_hint_button.place(x = 475, y = 330, width = 195, height = 30)

        WindowComponents.view_relevant_hint_button = Button(return_frame, text = "View Relevant Hint", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.view_relevant_hint_button.place(x = 475, y = 365, width = 195, height = 30)

        # Answer Area (Set by each Question Type)

        WindowComponents.submit_answer = Button(return_frame, text = "Submit Answer", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.submit_answer.place(x = 25, y = 195, width = 435, height = 30)

        WindowComponents.review_last_question = Button(return_frame, text = f"Review Last Question", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.review_last_question.place(x = 25, y = 330, width = 215, height = 30)

        WindowComponents.review_next_question = Button(return_frame, text = f"Review Next Question (If Applicable)", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.review_next_question.place(x = 245, y = 330, width = 215, height = 30)

        WindowComponents.exit_quiz_button = Button(return_frame, text = f"Exit Quiz", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.exit_quiz_button.place(x = 25, y = 365, width = 435, height = 30)

        return return_frame

    def insert_image() -> Toplevel: return None

    def create_closed_question_view(image_question: bool = False) -> None:
        WindowComponents.question_view = QuestionDesign.create_question_view_template()
        # if image_question: WindowDesign.insert_image()
        
        frame_width: int = 695
        frame_height: int = 420

        WindowComponents.question_view.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.position_frame(WindowComponents.question_view, [frame_width, frame_height])

        WindowComponents.view_relevant_hint_button.config(text = "Use 50/50 Hint")

        x_values: int = [25, 245, 25, 245]
        y_values: int = [195, 195, 245, 245]

        WindowComponents.closed_answer_buttons.clear()
        answer_button: Button

        for i in range(4):
            answer_button = Button(WindowComponents.question_view, text = f"Answer {i + 1}", wraplength = 175, bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
            answer_button.place(x = x_values[i], y = y_values[i] if not image_question else y_values[i] + 310, width = 215, height = 45)

            WindowComponents.closed_answer_buttons.append(answer_button)

        WindowComponents.submit_answer.place(y = 295 if not image_question else 605)

        if image_question:
            WindowComponents.review_last_question.place(y = 640)
            WindowComponents.review_next_question.place(y = 640)
            WindowComponents.exit_quiz_button.place(y = 675)

        WindowComponents.question_view.update()
        WindowComponents.question_view.deiconify()
        WindowComponents.make_active(WindowComponents.question_view)

    def create_open_question_view(image_question: bool = False) -> None:
        WindowComponents.question_view = QuestionDesign.create_question_view_template()
        # if image_question: WindowDesign.insert_image()
        
        frame_width: int = 695
        frame_height: int = 420

        WindowComponents.question_view.geometry(f"{frame_width}x{frame_height}")
        WindowComponents.position_frame(WindowComponents.question_view, [frame_width, frame_height])

        WindowComponents.view_relevant_hint_button.config(text = "Provide Word Hint")

        WindowComponents.open_answer_entry = Text(WindowComponents.question_view, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.open_answer_entry.place(x = 25, y = 195, width = 435, height = 95)

        WindowComponents.submit_answer.place(y = 295 if not image_question else 540)

        # WindowComponents.topics_shroud.place(height = 305)

        # WindowComponents.review_last_question.place(y = 265)
        # WindowComponents.review_next_question.place(y = 265)
        # WindowComponents.exit_quiz_button.place(y = 300)

        # WindowComponents.view_text_hint_button.place(x = 25, y = 335, width = 435)
        # WindowComponents.view_relevant_hint_button.place(y = 335)

        if image_question:
            WindowComponents.review_last_question.place(y = 575)
            WindowComponents.review_next_question.place(y = 575)
            WindowComponents.exit_quiz_button.place(y = 610)

        WindowComponents.question_view.update()
        WindowComponents.question_view.deiconify()
        WindowComponents.make_active(WindowComponents.question_view)

    def create_order_question_view(image_question: bool = False) -> None:
        WindowComponents.question_view = QuestionDesign.create_question_view_template()
        if image_question: QuestionDesign.insert_image()

        WindowComponents.topics_shroud.place(height = 410)

        WindowComponents.submit_answer.place(y = 405)
        WindowComponents.view_text_hint_button.place(y = 440)
        WindowComponents.view_relevant_hint_button.place(y = 475)

        WindowComponents.review_last_question.place(y = 440)
        WindowComponents.review_next_question.place(y = 440)
        WindowComponents.exit_quiz_button.place(y = 475)

        # Insert Answer Entries
        #  Entry (Input) + Label (Answer)

        x_values: list[int] = [25, 245]
        y_values: list[int] = [195, 230, 265, 300, 335, 370]

        position_entry: Entry
        answer_output: Label

        WindowComponents.order_answer_entries.clear()

        for i in range(2):
            for j in range(6):
                position_entry = Entry(WindowComponents.question_view, bg = WindowComponents.entry_colours[1].colour_code, fg = WindowComponents.entry_colours[0].colour_code, font = WindowComponents.main_font)
                position_entry.place(x = x_values[i], y = y_values[j], width = 40, height = 30)
                
                answer_output = Label(WindowComponents.question_view, bg = WindowComponents.entry_colours[0].colour_code, fg = WindowComponents.entry_colours[1].colour_code, font = WindowComponents.main_font)
                answer_output.place(x = x_values[i] + 40, y = y_values[j], width = 175, height = 30)

                WindowComponents.order_answer_entries.append([position_entry, answer_output])

        WindowComponents.question_view.update()
        WindowComponents.question_view.deiconify()


    # Finish Quiz Page

    def make_finish_quiz_page(window: Tk) -> None:
        frame = Toplevel(window)

        frame_width: int = 245
        frame_height: int = 220 # 400

        frame.geometry(f"{frame_width}x{frame_height}")
        frame.config(bg = WindowComponents.window_colours[0].colour_code)

        WindowComponents.position_frame(frame, [frame_width, frame_height])
        WindowComponents.make_active(frame)

        score: float = WindowComponents.current_quiz.current_score
        max: float = WindowComponents.current_quiz.theoretical_max

        percentage: float = round((score / max) * 100, 1)
 
        WindowComponents.current_quiz.score_percentage = percentage

        label_message: str = ""

        if percentage >= 80: label_message = "Congratulations!"
        elif percentage >= 60: label_message = "Well Done!"
        else: label_message = "Better Luck Next Time!"

        # Header Label
        message_label: Label = Label(frame, text = label_message, bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        message_label.place(x = 25, y = 25, width = 195, height = 30)

        # Score / Percentage
        score_header: Label = Label(frame, text = "Score:", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        score_header.place(x = 25, y = 60, width = 50, height = 30)

        score_output: Label = Label(frame, text = f"{score}/{max}", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        score_output.place(x = 80, y = 60, width = 70, height = 30)

        percentage_output: Label = Label(frame, text = f"{percentage}%", bg = WindowComponents.label_colours[0].colour_code, fg = WindowComponents.label_colours[1].colour_code, font = WindowComponents.main_font)
        percentage_output.place(x = 150, y = 60, width = 70, height = 30)

        # Retake Quiz Button
        WindowComponents.retake_quiz_button = Button(frame, text = "Retake Quiz", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.retake_quiz_button.place(x = 25, y = 95, width = 195, height = 30)

        # Review Quiz Button
        WindowComponents.review_quiz_button_finish = Button(frame, text = "Review Quiz", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.review_quiz_button_finish.place(x = 25, y = 130, width = 195, height = 30)

        # Exit Quiz / Return to Setup Page Button
        WindowComponents.exit_quiz_button_finish = Button(frame, text = "Exit Quiz", bg = WindowComponents.button_colours[0].colour_code, fg = WindowComponents.button_colours[1].colour_code, font = WindowComponents.main_font)
        WindowComponents.exit_quiz_button_finish.place(x = 25, y = 165, width = 195, height = 30)

        WindowComponents.finish_quiz_page = frame

