from typing import Dict, List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from models import Meal, Order
from services.order import list_order_meals, list_user_orders


class CallbackKeywords(BaseModel):
    order: str = "1_order_"
    meals: str = "2_meals_"


callbackKeywords = CallbackKeywords()


async def orders_keyboard(session: AsyncSession, user_id: int) -> InlineKeyboardMarkup:
    orders: List[Order] = await list_user_orders(user_id, session)
    keyword = callbackKeywords.order

    buttons = []
    for order in orders:
        buttons.append([
            InlineKeyboardButton(
                text=f"Замовлення №{order.id}", callback_data=f"{keyword}data_{order.id}"),
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def order_meals_keyboard(session: AsyncSession, order_id: int) -> InlineKeyboardMarkup:
    meals: List[Meal] = await list_order_meals(order_id, session)
    keyword = callbackKeywords.meals

    buttons = []
    for meal in meals:
        buttons.append([
            InlineKeyboardButton(
                text=f"{meal.name}", callback_data=f"{keyword}data_{meal.id}_{order_id}")
        ])

    buttons.append([
        InlineKeyboardButton(
            text="⏪ Назад", callback_data=f"{keyword}back_{order_id}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
