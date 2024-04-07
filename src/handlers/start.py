from aiogram import Router
from aiogram.filters import CommandStart
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from services.user import register_user
from services.messages import messageBuilder
from models import User
from keyboards.reply.home import home_keyboard

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: types.Message, session: AsyncSession, user: User) -> None:
    # check if user exists
    if user:
        return await message.answer(
            messageBuilder.start_welcome_back(user.first_name), 
            reply_markup=home_keyboard(user.is_manager)
        )
    
    new_user = await register_user(message.from_user, session)

    await message.answer(
        messageBuilder.start_welcome(new_user.first_name), 
        reply_markup=home_keyboard(new_user.is_manager)
    )
