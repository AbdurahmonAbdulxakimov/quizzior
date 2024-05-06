from telegram.ext import (
    ConversationHandler, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from tgbot.handlers.quiz import handlers as quiz_handlers
from tgbot.handlers.quiz import static_text as quiz_static_text


conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("search", quiz_handlers.search_quiz),
        # CommandHandler("start_quiz", quiz_handlers.start_quiz),
    ],
    states={
        # quiz_static_text.state.get('start_quiz'): [
        #     CallbackQueryHandler(quiz_handlers.play),
        # ]
    },
    fallbacks=[],
)