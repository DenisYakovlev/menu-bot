from typing import Dict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core import logger
from services.meal import list_menu_meal_by_type, get_meal_from_ids


class CallbackKeywords(BaseModel):
    choose_menu: str = "1_ch_menu_"
    check: str = "2_ch_check_"


callbackKeywords = CallbackKeywords()
    

async def menu_keyboard(session: AsyncSession, menu_id: int, state_data: Dict) -> InlineKeyboardMarkup:
    """
        Display keyboard for meal selections
    """
    current_type = state_data["types"][state_data["current_type_id"]]
    meals = await list_menu_meal_by_type(session, menu_id, current_type["id"])
    keyword = callbackKeywords.choose_menu

    buttons = []

    # meal buttons
    for meal in meals:
        meal_is_choosen = meal.id in [meal["id"] for meal in state_data["choosen_meals"]]

        buttons.append([
            InlineKeyboardButton(text=f"{meal.name} - {meal.price} грн", callback_data=f"{keyword}data_{meal.id}_{menu_id}"),
            InlineKeyboardButton(text=f"❌ Видалити", callback_data=f"{keyword}remove_{meal.id}_{menu_id}") \
                if meal_is_choosen else InlineKeyboardButton(text="➕ Додати страву", callback_data=f"{keyword}add_{meal.id}_{menu_id}")
        ])

    block_button = InlineKeyboardButton(
        text="⛔️", callback_data=f"{keyword}block"
    )

    # pagination button
    buttons.append([
        InlineKeyboardButton(text="⏪", callback_data=f"{keyword}previous_{meal.id}_{menu_id}") \
            if state_data["has_previous_type"] else block_button,

        InlineKeyboardButton(text=f"{current_type['name']}", callback_data=f"{keyword}current_{meal.id}_{menu_id}"),

        InlineKeyboardButton(text="⏩", callback_data=f"{keyword}next_{meal.id}_{menu_id}") \
            if state_data["has_next_type"] else block_button
    ])

    # global control buttons
    buttons.append([
        InlineKeyboardButton(text="❌ Скасувати", callback_data=f"{keyword}cancel"),
        InlineKeyboardButton(text="📝 Чек", callback_data=f"{keyword}check_{meal.id}_{menu_id}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def check_keyboard(session: AsyncSession, menu_id: int, state_data: Dict) -> InlineKeyboardMarkup:
    """
        Check keyboard
    """
    id_list = [meal["id"] for meal in state_data["choosen_meals"]]
    meals = await get_meal_from_ids(session, id_list)
    keyword = callbackKeywords.check

    buttons = []
    for meal in meals:
        buttons.append([
            InlineKeyboardButton(text=f"{meal.name} - {meal.price} грн", callback_data=f"{keyword}data__{menu_id}"),
            InlineKeyboardButton(text="❌ Видалити", callback_data=f"{keyword}remove_{meal.id}_{menu_id}")
        ])

    buttons.append([
        InlineKeyboardButton(text="⏪ Назад", callback_data=f"{keyword}back_{menu_id}"),
        InlineKeyboardButton(text="❌ Скасувати", callback_data=f"{callbackKeywords.choose_menu}cancel"),
        InlineKeyboardButton(text="✅ Підтвердити", callback_data=f"{keyword}confirm_{menu_id}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
