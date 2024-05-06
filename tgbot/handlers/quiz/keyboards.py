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


def make_keyboard_for_start_quiz() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton("Ready", callback_data="play"),
    ]]

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_quiz_question(answers) -> InlineKeyboardMarkup:
    buttons = []

    for answer in answers:
        buttons.append([InlineKeyboardButton(answer.title, callback_data=f"play {answer.id}")])

    return InlineKeyboardMarkup(buttons)
