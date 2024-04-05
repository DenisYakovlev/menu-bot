from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from services.meal import list_meal_types
from models.meal_type import MealType
from aiogram.types import CallbackQuery


async def meal_type_keyboard(session: AsyncSession) -> InlineKeyboardMarkup:
    """
        Inline Markup for meal types
    """

    meal_types: List[MealType] = await list_meal_types(session)

    buttons = []
    for type in meal_types:
        buttons.append([InlineKeyboardButton(text=type.name, callback_data=str(f"meal_type_{type.id}"))])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
