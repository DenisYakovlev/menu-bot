from typing import List
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from models import User, Order
from sqlalchemy.ext.asyncio import AsyncSession
from filters.auth import AuthorizedOnly
from keyboards.inline.orders import orders_keyboard, order_meals_keyboard, callbackKeywords
from services.messages import messageBuilder
from core.loader import bot
from services.order import list_order_meals


router = Router(name="orders")


@router.message(F.text == "📝 Мої замовлення", AuthorizedOnly())
async def orders(message: Message, user: User, session: AsyncSession) -> None:
    await message.answer(
        messageBuilder.orders(),
        reply_markup=await orders_keyboard(session, user.id)
    )


@router.callback_query(F.data.startswith(callbackKeywords.order + "data"))
async def process_data(callback_query: CallbackQuery, session: AsyncSession) -> None:
    callback_data = callback_query.data[len(callbackKeywords.order + "data_"):]
    order_id = int(callback_data)

    await bot.edit_message_text(
        messageBuilder.orders_meals(order_id),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await order_meals_keyboard(session, order_id)
    )

@router.callback_query(F.data.startswith(callbackKeywords.meals + "back"))
async def process_back(callback_query: CallbackQuery, session: AsyncSession) -> None:
    await bot.edit_message_text(
        messageBuilder.orders(),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await orders_keyboard(session, callback_query.from_user.id)
    )