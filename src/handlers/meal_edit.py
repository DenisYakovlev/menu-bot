from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from filters.manager import ManagerOnly
from keyboards.inline.meal_edit import meal_edit_keyboard
from models import User
from services.messages import messageBuilder

router = Router(name="meal_edit")


@router.message(F.text == "🖊 Редагувати страву", ManagerOnly())
async def meal_edit(message: Message, user: User, session: AsyncSession) -> None:
    await message.answer(
        messageBuilder.meal_edit(),
        reply_markup=await meal_edit_keyboard(session)
    )
