from aiogram import F, Router
from aiogram.types import Message

router = Router(name="test")


@router.message(F.text.lower() == "test")
async def start_handler(message: Message) -> None:
    await message.answer("testing")
