from typing import Dict, List
import asyncio

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pydantic import BaseModel
from models import Meal
from sqlalchemy.ext.asyncio import AsyncSession
from services.meal import list_meals, get_meal, get_meal_type


class CallbackKeywords(BaseModel):
    edit: str = "1_meal_edit_"
    edit_meal: str = "2_meal_edit_"


callbackKeywords = CallbackKeywords()


async def meal_edit_keyboard(session: AsyncSession) -> InlineKeyboardMarkup:
    keyword = callbackKeywords.edit
    meals: List[Meal] = await list_meals(session)

    buttons = []
    for meal in meals:
        buttons.append([
            InlineKeyboardButton(text=f"{meal.name}", callback_data=f"{keyword}data_{meal.id}"),
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def meal_edit_detailed_keyboard(session: AsyncSession, meal_id: int) -> InlineKeyboardMarkup:
    keyword = callbackKeywords.edit_meal
    meal, meal_type = await asyncio.gather(
        get_meal(session, meal_id),
        get_meal_type(session, meal_id)
    )

    buttons = [
        [InlineKeyboardButton(text=f"Назва", callback_data=f"{keyword}blank"), InlineKeyboardButton(text=f"{meal.name}", callback_data=f"{keyword}name_{meal_id}")],
        [InlineKeyboardButton(text=f"Ціна", callback_data=f"{keyword}blank"), InlineKeyboardButton(text=f"{meal.price}", callback_data=f"{keyword}price_{meal_id}")],
        [InlineKeyboardButton(text=f"Зображення", callback_data=f"{keyword}blank"), InlineKeyboardButton(text=f"{meal.img_url}", callback_data=f"{keyword}img_url_{meal_id}")],
        [InlineKeyboardButton(text=f"Тип", callback_data=f"{keyword}blank"), InlineKeyboardButton(text=f"{meal_type.name}", callback_data=f"{keyword}type_{meal_id}")],
        [InlineKeyboardButton(text="⏮ Повернутися назад", callback_data=f"{keyword}back_{meal_id}")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)