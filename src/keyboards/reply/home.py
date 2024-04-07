from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def home_keyboard(is_manager: bool) -> ReplyKeyboardMarkup:
    """
        Home menu
    """

    user_buttons = [
        [KeyboardButton(text="🔖 Меню")],
        [KeyboardButton(text="📝 Мої замовлення")],
        [KeyboardButton(text="⚙️ Налаштування")]
    ]

    manager_buttons = [
        [KeyboardButton(text="📑 Сплатити замовлення")]
    ]

    buttons = manager_buttons + user_buttons if is_manager else user_buttons

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)