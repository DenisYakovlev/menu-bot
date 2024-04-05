from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def settings_keyboard() -> ReplyKeyboardMarkup:
    """
        settings menu
    """

    buttons = [
        [KeyboardButton(text="👤 Надати контанки", request_contact=True)],
        [KeyboardButton(text="🧑‍💻 Змінити статус")],
        [KeyboardButton(text="📑 Повна інформація")],
        [KeyboardButton(text="⏮ Головне меню")]
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)