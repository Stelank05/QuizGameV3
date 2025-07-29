# Generic Imports
import math
import os

from tkinter import messagebox

# Custom Imports
from controls.file_handler import *
from controls.sort_functions import *

from classes.audio import Audio
from classes.colour import Colour
from classes.past_quiz import PastQuiz
from classes.player import Player
from classes.topic import Topic

from questions.question_base import BaseQuestion
from questions.question_closed import ClosedQuestion
from questions.question_open import OpenQuestion
from questions.question_order import OrderQuestion

class CommonData:
    min_password_length: int = 10
    
    root_folder: str
    setup_folder: str

    audio_folder: str
    guests_folder: str
    images_folder: str
    player_folder: str
    question_folder: str
    topics_folder: str

    audio_file: str
    colour_file: str

    audio_list: list[Audio] = []
    colour_list: list[Colour] = []
    topic_list: list[Topic] = []

    players: list[Player] = []
    guests: list[Player] = []

    usable_questions: list[BaseQuestion] = []
    discarded_questions: list[BaseQuestion] = []

    past_quizzes: list[PastQuiz] = []

    audio_names: list[str] = []
    colour_names: list[str] = []
    topic_names: list[str] = []


    # Setup

    def setup() -> None:
        CommonData.root_folder = get_root()
        CommonData.setup_folder = os.path.join(CommonData.root_folder, "setup")

        # Set Files + Folders
        CommonData.audio_folder = os.path.join(CommonData.setup_folder, "audios")
        CommonData.guests_folder = os.path.join(CommonData.setup_folder, "guests")
        CommonData.images_folder = os.path.join(CommonData.setup_folder, "images")
        CommonData.player_folder = os.path.join(CommonData.setup_folder, "players")
        CommonData.question_folder = os.path.join(CommonData.setup_folder, "questions")
        CommonData.topics_folder = os.path.join(CommonData.setup_folder, "topics")

        CommonData.audio_file = os.path.join(CommonData.setup_folder, "audio data.csv")
        CommonData.colour_file = os.path.join(CommonData.setup_folder, "colour data.csv")

        CommonData.load_audios()
        CommonData.load_colours()
        CommonData.load_topics()

        CommonData.load_questions()
        #CommonData.display_questions()
        #CommonData.update_topics()

        CommonData.load_players()
        CommonData.load_guest_players()

        CommonData.load_past_quizzes()


    # Loaders

    def load_audios() -> None:
        audios: list[str] = read_file(CommonData.audio_file)

        audio_data: list[str]

        for i in range(len(audios)):
            audio_data = audios[i].split(',')

            CommonData.audio_list.append(Audio(audio_data, os.path.join(CommonData.audio_folder, audio_data[2])))
            CommonData.audio_names.append(CommonData.audio_list[-1].audio_name)

    def load_colours() -> None:
        colours: list[str] = read_file(CommonData.colour_file)

        for colour in colours:
            CommonData.colour_list.append(Colour(colour.split(',')))
            CommonData.colour_names.append(CommonData.colour_list[-1].colour_name)

    def load_players() -> None:
        player_files: list[str] = get_files_in_folder(CommonData.player_folder, ".json")

        for player_file in player_files:CommonData.players.append(Player("Player", read_json_file(os.path.join(CommonData.player_folder, player_file))))

    def load_guest_players() -> None:
        player_files: list[str] = get_files_in_folder(CommonData.guests_folder, ".json")

        for player_file in player_files:CommonData.players.append(Player("Guest", read_json_file(os.path.join(CommonData.player_folder, player_file))))

    def load_topics() -> None:
        topic_files: list[str] = get_files_in_folder(CommonData.topics_folder, ".json")

        for topic_file in topic_files:
            CommonData.topic_list.append(Topic(read_json_file(os.path.join(CommonData.topics_folder, topic_file))))
            CommonData.topic_names.append(CommonData.topic_list[-1].topic_id)

    def load_questions() -> None: #This needs entirely rewriting lol
        question_files: list[str] = get_files_in_folder(CommonData.question_folder, ".json")

        new_question: BaseQuestion
        question_data: dict

        for question_file in question_files:
            question_data = read_json_file(os.path.join(CommonData.question_folder, question_file))

            match question_data["Question Type"]:
                case "Closed": new_question = ClosedQuestion(question_data)
                case "Open": new_question = OpenQuestion(question_data)
                case "Order": new_question = OrderQuestion(question_data)

            if new_question.discarded: CommonData.discarded_questions.append(new_question)
            else: CommonData.usable_questions.append(new_question)
  
    def update_topics(current_question: BaseQuestion) -> None:
        current_topic: Topic
        
        for topic in current_question.question_topics:
            current_topic = CommonData.get_topic_from_id(topic, 0, len(CommonData.topic_list) - 1)
            
            current_topic.questions.append(current_question.question_id)
            current_topic.total_questions += 1

    def load_past_quizzes() -> None:
        print("Load Past Quizzes")


    # Getters

    def get_audio_from_id(audio_id: str, start_index: int, end_index: int) -> Audio:
        id_sort_audios(CommonData.audio_list)
        
        if start_index > end_index: return None
        
        mid_point: int = math.floor((start_index + end_index) / 2)

        # if mid_point < 0 or mid_point > len(CommonData.audio_list)

        if CommonData.audio_list[mid_point].audio_id == audio_id: return CommonData.audio_list[mid_point]
        elif CommonData.audio_list[mid_point].audio_id > audio_id: return CommonData.get_audio_from_id(audio_id, start_index, mid_point - 1)
        else: return CommonData.get_audio_from_id(audio_id, mid_point + 1, end_index)

    def get_audio_from_name(audio_name: str, start_index: int, end_index: int) -> Audio:
        name_sort_audios(CommonData.audio_list)
        
        if start_index > end_index: return None
        
        mid_point: int = math.floor((start_index + end_index) / 2)

        if CommonData.audio_list[mid_point].audio_name == audio_name: return CommonData.audio_list[mid_point]
        elif CommonData.audio_list[mid_point].audio_name > audio_name: return CommonData.get_audio_from_name(audio_name, start_index, mid_point - 1)
        else: return CommonData.get_audio_from_name(audio_name, mid_point + 1, end_index)

    def get_colour_from_id(colour_id: str, start_index: int, end_index: int) -> Colour:
        id_sort_colours(CommonData.colour_list)

        if start_index > end_index: return None
        
        mid_point: int = math.floor((start_index + end_index) / 2)

        if CommonData.colour_list[mid_point].colour_id == colour_id: return CommonData.colour_list[mid_point]
        elif CommonData.colour_list[mid_point].colour_id > colour_id: return CommonData.get_colour_from_id(colour_id, start_index, mid_point - 1)
        else: return CommonData.get_colour_from_id(colour_id, mid_point + 1, end_index)
    
    def get_colour_from_name(colour_name: str, start_index: int, end_index: int) -> Colour:
        name_sort_colours(CommonData.colour_list)

        if start_index > end_index: return None
        
        mid_point: int = math.floor((start_index + end_index) / 2)

        if CommonData.colour_list[mid_point].colour_name == colour_name: return CommonData.colour_list[mid_point]
        elif CommonData.colour_list[mid_point].colour_name > colour_name: return CommonData.get_colour_from_name(colour_name, start_index, mid_point - 1)
        else: return CommonData.get_colour_from_name(colour_name, mid_point + 1, end_index)

    def get_topic_from_id(topic_id: str, start_index: int, end_index: int) -> Topic:
        id_sort_topics(CommonData.topic_list)

        if start_index > end_index: return None
        
        mid_point: int = math.floor((start_index + end_index) / 2)

        if CommonData.topic_list[mid_point].topic_id == topic_id: return CommonData.topic_list[mid_point]
        elif CommonData.topic_list[mid_point].topic_id > topic_id: return CommonData.get_topic_from_id(topic_id, start_index, mid_point - 1)
        else: return CommonData.get_topic_from_id(topic_id, mid_point + 1, end_index)
    
    def get_topic_from_name(topic_name: str, start_index: int, end_index: int) -> Topic:
        name_sort_topics(CommonData.topic_list)

        if start_index > end_index: return None
        
        mid_point: int = math.floor((start_index + end_index) / 2)

        if CommonData.topic_list[mid_point].topic_name == topic_name: return CommonData.topic_list[mid_point]
        elif CommonData.topic_list[mid_point].topic_name > topic_name: return CommonData.get_topic_from_name(topic_name, start_index, mid_point - 1)
        else: return CommonData.get_topic_from_name(topic_name, mid_point + 1, end_index)
    
    def get_account_from_id(account_id: str, start_index: int, end_index: int) -> Player:
        id_sort_users(CommonData.players)

        if start_index > end_index: return None
        
        mid_point: int = math.floor((start_index + end_index) / 2)

        if CommonData.players[mid_point].user_id == account_id: return CommonData.players[mid_point]
        elif CommonData.players[mid_point].user_id > account_id: return CommonData.get_account_from_id(account_id, start_index, mid_point - 1)
        else: return CommonData.get_account_from_id(account_id, mid_point + 1, end_index)
    
    def get_account_from_name(account_name: str, start_index: int, end_index: int) -> Player:
        name_sort_users(CommonData.players)

        if start_index > end_index: return None
        
        mid_point: int = math.floor((start_index + end_index) / 2)

        if CommonData.players[mid_point].username == account_name: return CommonData.players[mid_point]
        elif CommonData.players[mid_point].username > account_name: return CommonData.get_account_from_name(account_name, start_index, mid_point - 1)
        else: return CommonData.get_account_from_name(account_name, mid_point + 1, end_index)
    
    def get_usable_question(question_id: str, start_index: int, end_index: int) -> BaseQuestion:
        sort_questions(CommonData.usable_questions)

        if start_index > end_index: return None
        
        mid_point: int = math.floor((start_index + end_index) / 2)

        if CommonData.usable_questions[mid_point].question_id == question_id: return CommonData.usable_questions[mid_point]
        elif CommonData.usable_questions[mid_point].question_id > question_id: return CommonData.get_usable_question(question_id, start_index, mid_point - 1)
        else: return CommonData.get_usable_question(question_id, mid_point + 1, end_index)
        
    def get_discarded_question(question_id: str, start_index: int, end_index: int) -> BaseQuestion:
        sort_questions(CommonData.discarded_questions)
        
        if start_index > end_index: return None
        
        mid_point: int = math.floor((start_index + end_index) / 2)

        if CommonData.discarded_questions[mid_point].question_id == question_id: return CommonData.discarded_questions[mid_point]
        elif CommonData.discarded_questions[mid_point].question_id > question_id: return CommonData.get_discarded_question(question_id, start_index, mid_point - 1)
        else: return CommonData.get_discarded_question(question_id, mid_point + 1, end_index)
        
    def get_question(question_id: str, question_list: list[BaseQuestion] = [], start_index: int = -1, end_index: int = -1) -> BaseQuestion:
        if question_list == []:
            question_list = CommonData.usable_questions + CommonData.discarded_questions
            sort_questions(question_list)
            
            start_index = 0
            end_index = len(question_list)

        if start_index > end_index: return None

        mid_point: int = math.floor((start_index + end_index) / 2)

        if question_list[mid_point].question_id == question_id: return question_list[mid_point]
        elif question_list[mid_point].question_id > question_id: return CommonData.get_question(question_id, question_list, start_index, mid_point - 1)
        else: return CommonData.get_question(question_id, question_list, mid_point + 1, end_index)

    def get_past_quiz(quiz_id: str, start_index: int, end_index: int) -> PastQuiz:
        return PastQuiz({})

    
    # Displayers (Mainly for Testing)

    def display_audios() -> None:
        print("Display Audios")
        
        for audio in CommonData.audio_list: print(f"{audio.audio_id} - {audio.audio_name} - {audio.audio_file}")

    def display_colours() -> None:
        print("Display Colours")
        
        for colour in CommonData.colour_list: print(f"{colour.colour_id} - {colour.colour_name} - {colour.colour_code} - {colour.protected}")

    def display_topics() -> None:
        print("Display Topics")
        
        for topic in CommonData.topic_list: print(f"{topic.topic_id} - {topic.topic_name} - {topic.topic_colours[0]} / {topic.topic_colours[1]}")
    
    def display_questions() -> None:
        print("Usable Questions")

        # for question in CommonData.usable_questions:
        #     question.display_question(); print()
        
        print("\nDiscarded Questions")

        # for quesion in CommonData.discarded_questions:
        #     quesion.display_question(); print()