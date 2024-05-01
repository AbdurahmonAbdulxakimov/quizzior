import datetime

from django.utils import timezone
from telegram import Update
from telegram.ext import CallbackContext

from users.models import User
from tgbot.handlers.quiz import static_text, keyboards


'''
Example:

def command_start(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    
    text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text, reply_markup=keyboards.start_created)
'''


