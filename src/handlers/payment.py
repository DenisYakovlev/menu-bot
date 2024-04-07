from typing import List
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, SuccessfulPayment
from sqlalchemy.ext.asyncio import AsyncSession
from filters.manager import ManagerOnly
from services.order import get_order, set_order_paid
from services.messages import messageBuilder
from keyboards.inline.payments import payments_keyboad, payments_invoice_keyboard, callbackKeywords
from core.loader import bot
from core.config import settings


router = Router(name="payment")


@router.message(F.text == "📑 Сплатити замовлення", ManagerOnly())
async def payment(message: Message, session: AsyncSession) -> None:
    await message.answer(
        messageBuilder.payments(),
        reply_markup=await payments_keyboad(session)
    )


@router.callback_query(F.data.startswith(callbackKeywords.payments + "data"))
async def process_invoice(callback_query: CallbackQuery, session: AsyncSession) -> None:
    callback_data = callback_query.data[len(callbackKeywords.payments + "data_"):]
    order_id = int(callback_data)
    order = await get_order(order_id, session)

    await bot.send_invoice(
        chat_id=callback_query.from_user.id,
        title=f"Оплата замовлення №{order.id}",
        description=messageBuilder.test_payment_description(),
        payload=f"order_id_{order_id}",
        provider_token=settings.PAYMENT_TOKEN,
        currency="UAH",
        prices=[
            LabeledPrice(label="Загальна вартість", amount=order.total_price * 100)
        ],
        reply_markup=await payments_invoice_keyboard(order, session)
    )

@router.callback_query(F.data.startswith(callbackKeywords.invoice + "back"))
async def process_invoice(callback_query: CallbackQuery, session: AsyncSession) -> None:
    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )


@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery) -> None:
    # TODO: Don't leave it so blank
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def process_payment(message: Message, session: AsyncSession) -> None:
    payment: SuccessfulPayment = message.successful_payment
    order_id = int(payment.invoice_payload[len("order_id_"):])

    await set_order_paid(order_id, session)

    await message.answer(
        messageBuilder.payments(),
        reply_markup=await payments_keyboad(session)
    )
