from aiogram import F, Router
from aiogram.types import Message

from filters.auth import AuthorizedOnly
from services.messages import messageBuilder
from models.user import User
from keyboards.reply.menu import menu_keyboard

router = Router(name="menu")


@router.message(F.text == "🔖 Меню", AuthorizedOnly())
async def menu(message: Message, user: User) -> None:
    await message.answer(
        messageBuilder.menu(),
        reply_markup=menu_keyboard(user.is_manager)
    )
