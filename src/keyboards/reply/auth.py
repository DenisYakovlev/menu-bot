from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def auth_keyboard() -> ReplyKeyboardMarkup:
    """
        Use during first user visit and start command
    """

    buttons = [
        [KeyboardButton(text="give contact", request_contact=True)],
        [KeyboardButton(text="skip")]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard