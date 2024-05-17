from django.utils import timezone
from django.db.models import Q

from telegram import Update, ParseMode
from telegram.ext import CallbackContext, ConversationHandler

from users.models import User
from quiz.models import Quiz, Question, Answer, UserQuizStatistic
from tgbot.handlers.quiz import static_text, keyboards


def cancel(update: Update, context: CallbackContext) -> None:
    msg = context.user_data["running_quiz"]
    msg.edit_text(text=static_text.quiz_stoped)
    context.user_data.clear()


def cancel_creation(update: Update, context: CallbackContext) -> int:
    context.user_data.pop("new_quiz", None)
    update.message.reply_text(text=static_text.cancel_creation)
    return ConversationHandler.END


def create_quiz(update: Update, context: CallbackContext) -> str:
    # Stop running quiz, before creating a new one
    if "running_quiz" in context.user_data.keys():
        msg = context.user_data["running_quiz"]
        msg.edit_text(text=static_text.quiz_stoped)

    update.message.reply_text(static_text.quiz_create_instructions)

    return static_text.state.get("create_quiz_title")


def quiz_create_title(update: Update, context: CallbackContext) -> str:
    title = update.message.text.strip()
    if not title:
        update.message.reply_text(text=static_text.quiz_title_error)
        return static_text.state.get("create_quiz_title")

    context.user_data["new_quiz"] = {
        "title": title,
        "category": None,
        "questions": [],
    }

    update.message.reply_text(static_text.quiz_create_category_instructions)

    return static_text.state.get("create_quiz_category")


def quiz_create_category(update: Update, context: CallbackContext) -> str:
    category = update.message.text.strip()
    if not category:
        update.message.reply_text(text=static_text.quiz_category_error)
        return static_text.state.get("create_quiz_category")

    context.user_data["new_quiz"]["category"] = category

    update.message.reply_text(static_text.quiz_create_questions_instructions)

    return static_text.state.get("create_quiz_question")


def quiz_create_question(update: Update, context: CallbackContext) -> str:
    """On receiving polls, reply to it by a closed poll copying the received poll"""
    actual_poll = update.effective_message.poll
    # Only need to set the question and options
    context.user_data["new_quiz"]["questions"].append(
        {
            "question": actual_poll.question,
            "options": [option.text for option in actual_poll.options],
            "correct_answer": actual_poll.options[actual_poll.correct_option_id].text,
        }
    )

    update.message.reply_text(static_text.quiz_question_added)

    return static_text.state.get("create_quiz_question")


def perform_create(update: Update, context: CallbackContext) -> int:
    new_quiz = context.user_data["new_quiz"]

    user = User.get_user(update, context)

    quiz = Quiz.objects.create(
        title=new_quiz.get("title"),
        category=new_quiz.get("category"),
        author=user,
    )
    for question in new_quiz.get("questions"):
        question_obj = Question.objects.create(title=question["question"], quiz=quiz)
        for option in question["options"]:
            Answer.objects.create(
                title=option,
                question=question_obj,
                is_correct=option == question["correct_answer"],
            )

    update.message.reply_text(static_text.creation_success)
    return ConversationHandler.END


def search_quiz(update: Update, context: CallbackContext) -> None:
    try:
        user_input = update.message.text.split("/search ")[1].strip()
        queries = (
            Q(title__icontains=user_input)
            | Q(category__icontains=user_input)
            | Q(author__username=user_input)
        )
        quizzes = Quiz.objects.filter(queries)

        if not quizzes:
            update.message.reply_text(text=static_text.quiz_not_found)
            return

        msg = ""
        for quiz in quizzes:
            msg += (
                f"\n=== Id: {quiz.id} ===\n"
                f"<strong>Title</strong>: {quiz.title}\n"
                f"<strong>Category</strong>: {quiz.Category}\n"
                f"<strong>Questions</strong>: {quiz.questions.count()}\n"
                f"<strong>Author</strong>: {quiz.author.username}\n"
            )
        update.message.reply_text(text=msg, parse_mode=ParseMode.HTML)
    except IndexError:
        update.message.reply_text(text=static_text.search_instructions)


def start_quiz(update: Update, context: CallbackContext) -> None:
    if "running_quiz" in context.user_data.keys():
        update.message.reply_text(text=static_text.running_quiz_warning)
        return
    try:
        user_input = update.message.text.split("/quiz ")[1].strip()
        quiz = Quiz.objects.get_or_none(id=int(user_input))

        if not quiz:
            update.message.reply_text(text=static_text.quiz_not_found)
            return

        context.user_data["quiz"] = quiz
        context.user_data["questions"] = quiz.questions.all()
        context.user_data["answers"] = []

        update.message.reply_text(
            text=static_text.make_text_for_start_quiz(quiz),
            parse_mode=ParseMode.HTML,
            reply_markup=keyboards.make_keyboard_for_start_quiz(),
        )
    except (IndexError, ValueError) as e:
        update.message.reply_text(text=static_text.start_quiz_instructions)


def play(update: Update, context: CallbackContext) -> None:
    # CallbackQueries need to be answered, even if no notification to the user is needed
    query = update.callback_query
    query.answer()

    # Update user answers
    try:
        if "running_quiz" not in context.user_data.keys():
            context.user_data["running_quiz"] = query.message
        if context.user_data["running_quiz"].message_id != query.message.message_id:
            raise KeyError
        if query.data != "play":
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
        context.user_data["questions"] = questions[1:]

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
    query.edit_message_text(
        text=static_text.make_quiz_statistics(user_quiz), parse_mode=ParseMode.HTML
    )
    context.user_data.clear()
