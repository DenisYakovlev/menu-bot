from aiogram import F, Router
from aiogram.exceptions import DetailedAiogramError
from aiogram.types import Contact, Message
from sqlalchemy.ext.asyncio import AsyncSession

from filters.auth import AuthorizedOnly
from keyboards.reply.settings import settings_keyboard
from models.user import User
from services.messages import messageBuilder
from services.user import change_user_status, update_user_from_contact

router = Router(name="settings")


@router.message(F.text == "⚙️ Налаштування", AuthorizedOnly())
async def settings(message: Message, user: User) -> None:
    response: str = messageBuilder.settings(
        user.phone_number,
        user.first_name,
        user.last_name,
        user.is_manager
    )

    await message.answer(response, reply_markup=settings_keyboard())


@router.message(F.text == "🧑‍💻 Змінити статус", AuthorizedOnly())
async def settings_become_manager(message: Message, user: User, session: AsyncSession) -> None:
    await change_user_status(user, session)

    await message.answer(
        messageBuilder.settings_status_update(user.is_manager),
        reply_markup=settings_keyboard()
    )


@router.message(F.text == "📑 Повна інформація", AuthorizedOnly())
async def settings_full_info(message: Message, user: User) -> None:
    await settings(message, user)


@router.message(F.contact, AuthorizedOnly())
async def settings_contact(message: Message, user: User, session: AsyncSession) -> None:
    contact: Contact = message.contact

    if user.id != contact.user_id:
        raise DetailedAiogramError("Ви надали не свій контакт!")

    await update_user_from_contact(user, contact, session)

    await message.answer(
        messageBuilder.settings_from_contact(),
        reply_markup=settings_keyboard()
    )
