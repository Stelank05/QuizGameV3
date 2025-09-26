from classes.audio import Audio
from classes.colour import Colour
from classes.guest import Guest
from classes.player import Player
from classes.topic import Topic

from questions.answer import Answer
from questions.question_base import BaseQuestion

from quiz.quiz_past import PastQuiz

def id_sort_audios(audio_list: list[Audio]) -> None:
    swap: bool

    for i in range(len(audio_list) - 1):
        swap = False

        for j in range(len(audio_list) - i - 1):
            if audio_list[j].audio_id > audio_list[j + 1].audio_id:
                swap = True
                audio_list[j], audio_list[j + 1] = audio_list[j + 1], audio_list[j]

        if not swap: break

    return audio_list

def name_sort_audios(audio_list: list[Audio]) -> None:
    swap: bool

    for i in range(len(audio_list) - 1):
        swap = False

        for j in range(len(audio_list) - i - 1):
            if audio_list[j].audio_name > audio_list[j + 1].audio_name:
                swap = True
                audio_list[j], audio_list[j + 1] = audio_list[j + 1], audio_list[j]

        if not swap: break

    return audio_list

def id_sort_colours(colour_list: list[Colour]) -> None:
    swap: bool

    for i in range(len(colour_list) - 1):
        swap = False

        for j in range(len(colour_list) - i - 1):
            if colour_list[j].colour_id > colour_list[j + 1].colour_id:
                swap = True
                colour_list[j], colour_list[j + 1] = colour_list[j + 1], colour_list[j]

        if not swap: break

def name_sort_colours(colour_list: list[Colour]) -> None:
    swap: bool

    for i in range(len(colour_list) - 1):
        swap = False

        for j in range(len(colour_list) - i - 1):
            if colour_list[j].colour_name > colour_list[j + 1].colour_name:
                swap = True
                colour_list[j], colour_list[j + 1] = colour_list[j + 1], colour_list[j]

        if not swap: break

def id_sort_topics(topic_list: list[Topic]) -> None:
    swap: bool

    for i in range(len(topic_list) - 1):
        swap = False

        for j in range(len(topic_list) - i - 1):
            if topic_list[j].topic_id > topic_list[j + 1].topic_id:
                swap = True
                topic_list[j], topic_list[j + 1] = topic_list[j + 1], topic_list[j]

        if not swap: break

def name_sort_topics(topic_list: list[Topic]) -> None:
    swap: bool

    for i in range(len(topic_list) - 1):
        swap = False

        for j in range(len(topic_list) - i - 1):
            if topic_list[j].topic_name > topic_list[j + 1].topic_name:
                swap = True
                topic_list[j], topic_list[j + 1] = topic_list[j + 1], topic_list[j]

        if not swap: break

def sort_questions(question_list: list[BaseQuestion]) -> None:
    swap: bool

    for i in range(len(question_list) - 1):
        swap = False

        for j in range(len(question_list) - i - 1):
            if question_list[j].question_id > question_list[j + 1].question_id:
                swap = True
                question_list[j], question_list[j + 1] = question_list[j + 1], question_list[j]

        if not swap: break

def id_sort_users(user_list: list[Player]) -> None:
    swap: bool

    for i in range(len(user_list) - 1):
        swap = False

        for j in range(len(user_list) - i - 1):
            if user_list[j].user_id > user_list[j + 1].user_id:
                swap = True
                user_list[j], user_list[j + 1] = user_list[j + 1], user_list[j]

        if not swap: break

def name_sort_users(user_list: list[Player]) -> None:
    swap: bool

    for i in range(len(user_list) - 1):
        swap = False

        for j in range(len(user_list) - i - 1):
            if user_list[j].username > user_list[j + 1].username:
                swap = True
                user_list[j], user_list[j + 1] = user_list[j + 1], user_list[j]

        if not swap: break

def id_sort_guests(guest_list: list[Guest]) -> None:
    swap: bool

    for i in range(len(guest_list) - 1):
        swap = False

        for j in range(len(guest_list) - i - 1):
            if guest_list[j].guest_id > guest_list[j + 1].guest_id:
                swap = True
                guest_list[j], guest_list[j + 1] = guest_list[j + 1], guest_list[j]

        if not swap: break

def sort_quizzes_id(quiz_list: list[PastQuiz]) -> None:
    swap: bool

    for i in range(len(quiz_list) - 1):
        swap = False

        for j in range(len(quiz_list) - i - 1):
            if quiz_list[j].quiz_id > quiz_list[j + 1].quiz_id:
                swap = True
                quiz_list[j], quiz_list[j + 1] = quiz_list[j + 1], quiz_list[j]

        if not swap: break


