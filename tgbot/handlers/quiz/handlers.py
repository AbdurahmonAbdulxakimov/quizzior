import datetime

from django.utils import timezone
from django.db.models import Q

from telegram import Update, ParseMode, Poll, Message, Chat
from telegram.ext import CallbackContext, ConversationHandler, ContextTypes

from users.models import User
from quiz.models import Quiz, Answer, UserQuizStatistic
from tgbot.handlers.quiz import static_text, keyboards


def cancel(update: Update, context: CallbackContext) -> None:
    msg = context.user_data['running_quiz']
    msg.edit_text(text=static_text.quiz_stoped)
    context.user_data.clear()


def search_quiz(update: Update, context: CallbackContext) -> None:
    try:
        user_input = update.message.text.split('/search ')[1]
        queries = Q(title__icontains=user_input) | Q(topic__icontains=user_input) | Q(author__username=user_input)
        quizzes = Quiz.objects.filter(queries)

        if not quizzes:
            update.message.reply_text(text=static_text.quiz_not_found)
            return

        msg = ''
        for quiz in quizzes:
            msg += (f'\n=== Id: {quiz.id} ===\n'
                    f'<strong>Title</strong>: {quiz.title}\n'
                    f'<strong>Topic</strong>: {quiz.topic}\n'
                    f'<strong>Questions</strong>: {quiz.questions.count()}\n'
                    f'<strong>Author</strong>: {quiz.author.username}\n')
        update.message.reply_text(text=msg, parse_mode=ParseMode.HTML)
    except IndexError:
        update.message.reply_text(text=static_text.search_instructions)


def start_quiz(update: Update, context: CallbackContext) -> None:
    if 'running_quiz' in context.user_data.keys():
        update.message.reply_text(text=static_text.running_quiz_warning)
        return
    try:
        user_input = update.message.text.split('/quiz ')[1].strip()
        quiz = Quiz.objects.get_or_none(id=int(user_input))

        if not quiz:
            update.message.reply_text(text=static_text.quiz_not_found)
            return

        context.user_data['quiz'] = quiz
        context.user_data["questions"] = quiz.questions.all()
        context.user_data["answers"] = []

        update.message.reply_text(text=static_text.make_text_for_start_quiz(quiz),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=keyboards.make_keyboard_for_start_quiz())
    except (IndexError, ValueError) as e:
        update.message.reply_text(text=static_text.start_quiz_instructions)


def play(update: Update, context: CallbackContext) -> None:
    # CallbackQueries need to be answered, even if no notification to the user is needed
    query = update.callback_query
    query.answer()

    # Update user answers
    try:
        if 'running_quiz' not in context.user_data.keys():
            context.user_data['running_quiz'] = query.message
        if context.user_data['running_quiz'].message_id != query.message.message_id:
            raise KeyError
        if query.data != 'play':
            answer_id = query.data.split("play ")[1].strip()
            user_answer = Answer.objects.get_or_none(id=answer_id)

            context.user_data["answers"].append(user_answer)
    except (TypeError, KeyError) as e:
        query.edit_message_text(text=static_text.quiz_stoped, parse_mode=ParseMode.HTML)
        context.user_data.clear()
        return

    # Render Question and answer options
    questions = context.user_data.get("questions")
    if questions:
        question = questions[0]
        question_answers = question.answers.all()

        # Update questions
        context.user_data['questions'] = questions[1:]

        answer_markup = keyboards.make_keyboard_for_quiz_question(question_answers)
        query.edit_message_text(text=f"{question.title}", reply_markup=answer_markup)
        return

    #  Save user statistics
    user = User.get_user(update, context)
    quiz = context.user_data.get("quiz")
    user_answers = context.user_data.get("answers")

    user_quiz = UserQuizStatistic.objects.get_or_create(user=user, quiz=quiz)[0]
    user_quiz.user_answers.set(user_answers)
    user_quiz.save()

    # Output Statistics
    query.edit_message_text(text=static_text.make_quiz_statistics(user_quiz), parse_mode=ParseMode.HTML)
    context.user_data.clear()
