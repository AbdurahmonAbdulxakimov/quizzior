from telegram.ext import (
    ConversationHandler,
    filters,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
)

from tgbot.handlers.quiz import handlers as quiz_handlers
from tgbot.handlers.quiz import static_text as quiz_static_text


conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("create_quiz", quiz_handlers.create_quiz),
    ],
    states={
        quiz_static_text.state.get("create_quiz_title"): [
            MessageHandler(Filters.text, quiz_handlers.quiz_create_title),
        ],
        quiz_static_text.state.get("create_quiz_category"): [
            MessageHandler(Filters.text, quiz_handlers.quiz_create_category),
        ],
        quiz_static_text.state.get("create_quiz_question"): [
            MessageHandler(Filters.poll, quiz_handlers.quiz_create_question),
        ],
    },
    fallbacks=[
        CommandHandler("cancel_creation", quiz_handlers.cancel_creation),
        CommandHandler("perform_create", quiz_handlers.perform_create),
    ],
)
