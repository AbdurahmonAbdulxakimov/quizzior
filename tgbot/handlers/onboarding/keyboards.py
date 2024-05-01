from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding import static_text


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    buttons = [[
        # InlineKeyboardButton(static_text, ...),
    ]]

    return InlineKeyboardMarkup(buttons)
