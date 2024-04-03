from aiogram import F, Router
from aiogram.types import Message

from core import redis_client


router = Router(name="redis_test")


@router.message(F.text.lower() == "test_redis")
async def test_start(message: Message):
    await redis_client.set("value", 1)
    await message.answer("testing redis")
    
@router.message(F.text.lower() == "test_redis_")
async def test_end(message: Message):
    data = await redis_client.get("value")
    await message.answer(f"{data}")
    
