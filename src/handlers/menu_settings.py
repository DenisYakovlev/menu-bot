from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from filters.manager import ManagerOnly
from keyboards.reply.menu_settings import menu_settings_keyboard
from models.user import User
from services.messages import messageBuilder


router = Router(name="menu_settings")


@router.message(F.text == "⚙️ Налаштування меню", ManagerOnly())
async def menu_settings(message: Message) -> None:
    await message.answer(
        messageBuilder.menu_settings(),
        reply_markup=menu_settings_keyboard()
    )


@router.message(F.text == "❌ Відмінити", ManagerOnly())
async def cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state:
        await state.clear()

    await menu_settings(message)


@router.message(F.text == "🖊 Редагувати страву", ManagerOnly())
async def meal_update(message: Message, user: User, session: AsyncSession) -> None:
    await message.answer("mock")

