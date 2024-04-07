from typing import Dict, List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from models import Order
from services.order import list_unpaid_orders
from models import Order


class CallbackKeywords(BaseModel):
    payments: str = "1_payments_"
    invoice: str = "2_invoce_"

callbackKeywords = CallbackKeywords()


async def payments_keyboad(session: AsyncSession) -> InlineKeyboardMarkup:
    keyword = callbackKeywords.payments
    orders: List[Order] = await list_unpaid_orders(session)

    buttons = []
    for order in orders:
        buttons.append([
            InlineKeyboardButton(
                text=f"Замовлення №{order.id} - {order.total_price} грн",
                callback_data=f"{keyword}data_{order.id}"
            )
        ])
        
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def payments_invoice_keyboard(order: Order, session: AsyncSession) -> InlineKeyboardMarkup:
    keyword = callbackKeywords.invoice

    buttons = [
        [InlineKeyboardButton(text=f"Сплатити {order.total_price} грн", pay=True)],
        [InlineKeyboardButton(text="❌ Скасувати", callback_data=f"{keyword}back")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)