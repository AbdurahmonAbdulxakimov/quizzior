"""
    Follow snake case
"""

quiz_create_instructions = (
    "Please send the title of your quiz.\n\n"
    'You can cancel creation (after you provide "title" and "category")\n'
    "by calling /cancel_creation command."
)
quiz_create_category_instructions = (
    "Please send the category that your quiz might belong to."
)
quiz_create_questions_instructions = (
    "Please send the question of your quiz. In form of Quiz Poll.\n"
    "You can send as many questions as you want.\n"
    "When you are done sending, call /perform_create command."
)
search_instructions = (
    "To search for quizes, type /search command with "
    "text separated by space. For example:\n\n"
    "/search irregular verbs"
)
start_quiz_instructions = (
    "To start Quiz, type /start_quiz command with "
    "id separated by space. For example:\n\n"
    "/start_quiz 777 "
)

creation_success = "Quiz created successfully✔️"
cancel_creation = "Quiz creation cancelled successfully✔️"
quiz_question_added = "Quiz question added successfully✔️"
quiz_title_error = "Please provide a valid title for your quiz❗"
quiz_category_error = "Please provide a valid category for your quiz❗"
quiz_not_found = "🤔 There is no quiz with that ID"
quiz_stoped = "Quiz stoped!"
running_quiz_warning = (
    "You have an unfinished quiz. Please finish creating your quiz or send /cancel."
)

state = {
    "create_quiz_title": "create_quiz_title",
    "create_quiz_category": "create_quiz_category",
    "create_quiz_question": "create_quiz_question",
}


"""
###################################
Reply message generator functions! 
###################################
"""


def make_quiz_info(quiz):
    return (
        f"<strong>=== Quiz information ===</strong>\n"
        f"<strong>Title</strong>: {quiz.title}\n"
        f"<strong>Category</strong>: {quiz.category}\n"
        f"<strong>Questions</strong>: {quiz.questions.count()}\n"
        f"<strong>Author</strong>: {quiz.author.username}\n"
    )


def make_text_for_start_quiz(quiz):
    return (
        f"🎲 Get ready for the quiz '{quiz.title}'\n\n"
        f"🖊 {quiz.questions.count()} questions\n"
        # f"⏱ 10 seconds per question\n"
        f"📰 Votes are visible to the quiz owner\n\n"
        f"🏁 Press the button below when you are ready."
    )


def make_quiz_statistics(user_quiz):
    details = ""
    for question in user_quiz.quiz.questions.all():
        details += f"{question.title}\n"
        correct_answer = question.answers.get(is_correct=True)

        for answer in question.answers.all():
            if answer in user_quiz.user_answers.all():
                if answer.is_correct:
                    details += f"✅ <i>{answer.title}</i>\n\n"
                elif not answer.is_correct:
                    details += (
                        f"❌ <i><s>{answer.title}</s></i>\n"
                        f"✅ <i>{correct_answer.title}</i>\n\n"
                    )
                break

    txt = (
        f"🏁 The quiz '{user_quiz.quiz.title}' has finished!\n\n"
        f"✅ Correct – {user_quiz.correct_answers}\n"
        f"❌ Wrong – {user_quiz.wrong_answers}\n\n"
        f"<i>======= Details =======</i>\n\n"
        f"{details}\n"
    )

    return txt
