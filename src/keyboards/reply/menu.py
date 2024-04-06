from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def menu_keyboard(is_manager: bool) -> ReplyKeyboardMarkup:
    """
        Menu keyboard
    """

    user_buttons = [
        [KeyboardButton(text="🕒 Обрати меню на сьогодні")],
        [KeyboardButton(text="🕥 Обрати меню на завтра")],
        [KeyboardButton(text="⏮ Головне меню")]
    ]

    manager_buttons = [
        [KeyboardButton(text="⚙️ Налаштування меню")]
    ]

    buttons = manager_buttons + user_buttons if is_manager else user_buttons

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)