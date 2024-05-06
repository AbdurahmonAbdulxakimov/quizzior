'''
    Follow snake case
'''

search_instructions = "To search for quizes, type /search command with " \
                      "text separated by space. For example:\n\n" \
                      "/search irregular verbs"
start_quiz_instructions = "To start Quiz, type /start_quiz command with " \
                          "id separated by space. For example:\n\n" \
                          "/start_quiz 777 "

quiz_not_found = "🤔 There is no quiz with that ID."
quiz_stoped = "Quiz stoped!"
running_quiz_warning = "You have an unfinished quiz. Please finish creating your quiz or send /cancel."

state = {
    'start_quiz': 'start_quiz',
    'play_quiz': 'play_quiz',
}


def make_quiz_info(quiz):
    return (f'<strong>=== Quiz information ===</strong>\n'
            f'<strong>Title</strong>: {quiz.title}\n'
            f'<strong>Topic</strong>: {quiz.topic}\n'
            f'<strong>Questions</strong>: {quiz.questions.count()}\n'
            f'<strong>Author</strong>: {quiz.author.username}\n')


def make_text_for_start_quiz(quiz):
    return (f"🎲 Get ready for the quiz '{quiz.title}'\n\n"
            f"🖊 {quiz.questions.count()} questions\n"
            # f"⏱ 10 seconds per question\n"
            f"📰 Votes are visible to the quiz owner\n\n"
            
            f"🏁 Press the button below when you are ready.")


def make_quiz_statistics(user_quiz):
    details = ''
    for question in user_quiz.quiz.questions.all():
        details += f'{question.title}\n'
        correct_answer = question.answers.get(is_correct=True)

        for answer in question.answers.all():
            if answer in user_quiz.user_answers.all():
                if answer.is_correct:
                    details += f'✅ <i>{answer.title}</i>\n\n'
                elif not answer.is_correct:
                    details += (f'❌ <i><s>{answer.title}</s></i>\n'
                                f'✅ <i>{correct_answer.title}</i>\n\n')
                break

    txt = (f'🏁 The quiz \'{user_quiz.quiz.title}\' has finished!\n\n'
           f'✅ Correct – {user_quiz.correct_answers}\n'
           f'❌ Wrong – {user_quiz.wrong_answers}\n\n'
           f'<i>======= Details =======</i>\n\n'
           f'{details}\n')

    return txt
