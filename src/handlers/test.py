from aiogram import Router, F
from aiogram.types import Message

from models.user import User
from core import logger
from filters.auth import AuthorizedOnly


router = Router(name="test")

@router.message(F.text.lower() == "test", AuthorizedOnly())
async def test_handler(message: Message, user: User):
    logger.debug(f"{user}")
    await message.answer("testing")