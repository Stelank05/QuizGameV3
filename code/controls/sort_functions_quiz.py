from quiz.quiz_past import PastQuiz

# Past Quiz Sorts

def order_correct(quiz_list: list[PastQuiz]) -> None:
    swap: bool

    for i in range(len(quiz_list) - 1):
        swap = False

        for j in range(len(quiz_list) - i - 1):
            if quiz_list[j].correct_count < quiz_list[j + 1].correct_count:
                swap = True
                quiz_list[j], quiz_list[j + 1] = quiz_list[j + 1], quiz_list[j]

        if not swap: break

def order_incorrect(quiz_list: list[PastQuiz]) -> None:
    swap: bool

    for i in range(len(quiz_list) - 1):
        swap = False

        for j in range(len(quiz_list) - i - 1):
            if quiz_list[j].incorrect_count < quiz_list[j + 1].incorrect_count:
                swap = True
                quiz_list[j], quiz_list[j + 1] = quiz_list[j + 1], quiz_list[j]

        if not swap: break

def order_correct_percentage(quiz_list: list[PastQuiz]) -> None:
    swap: bool

    for i in range(len(quiz_list) - 1):
        swap = False

        for j in range(len(quiz_list) - i - 1):
            if quiz_list[j].correct_percentage < quiz_list[j + 1].correct_percentage:
                swap = True
                quiz_list[j], quiz_list[j + 1] = quiz_list[j + 1], quiz_list[j]

        if not swap: break

def order_score(quiz_list: list[PastQuiz]) -> None:
    swap: bool

    for i in range(len(quiz_list) - 1):
        swap = False

        for j in range(len(quiz_list) - i - 1):
            if quiz_list[j].score < quiz_list[j + 1].score:
                swap = True
                quiz_list[j], quiz_list[j + 1] = quiz_list[j + 1], quiz_list[j]

        if not swap: break

def order_max_score(quiz_list: list[PastQuiz]) -> None:
    swap: bool

    for i in range(len(quiz_list) - 1):
        swap = False

        for j in range(len(quiz_list) - i - 1):
            if quiz_list[j].max_score < quiz_list[j + 1].max_score:
                swap = True
                quiz_list[j], quiz_list[j + 1] = quiz_list[j + 1], quiz_list[j]

        if not swap: break

def order_score_percentage(quiz_list: list[PastQuiz]) -> None:
    swap: bool

    for i in range(len(quiz_list) - 1):
        swap = False

        for j in range(len(quiz_list) - i - 1):
            if quiz_list[j].percentage < quiz_list[j + 1].percentage:
                swap = True
                quiz_list[j], quiz_list[j + 1] = quiz_list[j + 1], quiz_list[j]

        if not swap: break

def order_hints_used(quiz_list: list[PastQuiz]) -> None:
    swap: bool

    for i in range(len(quiz_list) - 1):
        swap = False

        for j in range(len(quiz_list) - i - 1):
            if quiz_list[j].total_hints_used < quiz_list[j + 1].total_hints_used:
                swap = True
                quiz_list[j], quiz_list[j + 1] = quiz_list[j + 1], quiz_list[j]

        if not swap: break

def order_quiz_length_hl(quiz_list: list[PastQuiz]) -> None:
    swap: bool

    for i in range(len(quiz_list) - 1):
        swap = False

        for j in range(len(quiz_list) - i - 1):
            if len(quiz_list[j].questions) < len(quiz_list[j + 1].questions):
                swap = True
                quiz_list[j], quiz_list[j + 1] = quiz_list[j + 1], quiz_list[j]

        if not swap: break

def order_quiz_length_lh(quiz_list: list[PastQuiz]) -> None:
    swap: bool

    for i in range(len(quiz_list) - 1):
        swap = False

        for j in range(len(quiz_list) - i - 1):
            if len(quiz_list[j].questions) > len(quiz_list[j + 1].questions):
                swap = True
                quiz_list[j], quiz_list[j + 1] = quiz_list[j + 1], quiz_list[j]

        if not swap: break