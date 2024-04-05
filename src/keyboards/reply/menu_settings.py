from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def menu_settings_keyboard() -> ReplyKeyboardMarkup:
    """
        Menu keyboard
    """

    buttons = [
        [KeyboardButton(text="🛠 Створити меню"), KeyboardButton(text="🖊 Редагувати меню")],
        [KeyboardButton(text="🛠 Створити страву"), KeyboardButton(text="🖊 Редагувати страву")],
        [KeyboardButton(text="⏮ Головне меню")]
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def entity_create_keyboard() -> ReplyKeyboardMarkup:
    """
        Keyboard for creating new menu
    """

    buttons = [
        [KeyboardButton(text="❌ Відмінити")]
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
