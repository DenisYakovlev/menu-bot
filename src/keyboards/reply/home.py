from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def home_keyboard() -> ReplyKeyboardMarkup:
    """
        Home menu
    """

    buttons = [
        [KeyboardButton(text="🔖 Меню")],
        [KeyboardButton(text="⚙️ Налаштування")]
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)