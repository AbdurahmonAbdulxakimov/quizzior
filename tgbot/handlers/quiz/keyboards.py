from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.quiz import static_text

'''
Example:

def make_keyboard_for_() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(static_text, ...),
    ]]

    return InlineKeyboardMarkup(buttons)
'''

