from aiogram import F, Router
from aiogram.types import Message, ErrorEvent

from filters.auth import AuthorizedOnly
from services.messages import messageBuilder
from keyboards.reply.home import home_keyboard
from core.loader import logger

router = Router(name="core")


@router.message(F.text == "⏮ Головне меню", AuthorizedOnly())
async def main_menu(message: Message) -> None:
    """
        back to home menu
    """

    await message.answer(
        messageBuilder.main_menu(),
        reply_markup=home_keyboard()
    )

@router.error(F.update.message.as_("message"))
async def error_handler(event: ErrorEvent, message: Message):
    error_str = str(event.exception)

    logger.critical(error_str)

    await message.answer(messageBuilder.error(error_str))