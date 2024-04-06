from typing import Dict, List

from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from models.menu import Menu
from models.meal import Meal
from models.meal_type import MealType
from services.meal import list_meal_types, list_menu_meals, list_unused_meals
from services.menu import list_menus
from core import logger


class CallbackKeywords(BaseModel):
    meal_type: str = "1_meal_type_"
    menu_edit: str = "2_menu_"
    menu_meal_edit: str = "3_menu_meal_"
    menu_meal_add: str = "4_add_meal_"

callbackKeywords = CallbackKeywords()


async def meal_type_keyboard(session: AsyncSession) -> InlineKeyboardMarkup:
    """
        Inline Markup for meal types
    """
    keyword = callbackKeywords.meal_type

    meal_types: List[MealType] = await list_meal_types(session)

    buttons = []
    for type in meal_types:
        buttons.append([InlineKeyboardButton(
            text=type.name, callback_data=str(f"{keyword}{type.id}"))])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def menu_edit_keyboard(session: AsyncSession) -> InlineKeyboardMarkup:
    """
        Inline markup to list all menus
    """
    keyword = callbackKeywords.menu_edit

    menus: List[Menu] = await list_menus(session)
    
    buttons = []
    for menu in menus:

        buttons.append(
            [InlineKeyboardButton(text=menu.name, callback_data=str(f"{keyword}{menu.id}"))]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def menu_meal_edit_keyboard(session: AsyncSession, menu_id: int) -> InlineKeyboardMarkup:
    """
        Markup for managing meals in menu
    """
    keyword = callbackKeywords.menu_meal_edit
    meals: List[Meal] = await list_menu_meals(session, menu_id)

    buttons = []
    for meal in meals:
        buttons.append([
            InlineKeyboardButton(text=f"{meal.name} - {meal.price} грн", callback_data=f"{keyword}data_{menu_id}_{meal.id}"),
            InlineKeyboardButton(text="❌", callback_data=f"{keyword}delete_{menu_id}_{meal.id}")
        ])

    buttons.append(
        [InlineKeyboardButton(text="➕ Додати страву", callback_data=f"{keyword}new_{menu_id}")]
    )

    buttons.append(
        [InlineKeyboardButton(text="⏮ Повернутися назад", callback_data=f"{keyword}back")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def menu_meal_add_keyboard(session: AsyncSession, menu_id: int) -> InlineKeyboardMarkup:
    """
        Markup with all meals that are not in menu
    """
    keyword = callbackKeywords.menu_meal_add
    meals = await list_unused_meals(session, menu_id)

    buttons = []
    for meal in meals:
        cb_data = f"{keyword}data_{menu_id}_{meal.id}"

        buttons.append([
            InlineKeyboardButton(text=f"{meal.name} - {meal.price} грн", callback_data=cb_data),
            InlineKeyboardButton(text=f"➕ Додати", callback_data=cb_data)
        ])

    buttons.append(
        [InlineKeyboardButton(text="⏮ Повернутися назад", callback_data=f"{keyword}back_{menu_id}")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
