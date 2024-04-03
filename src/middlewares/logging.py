from typing import Any, Awaitable, Callable, Coroutine, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update, Message

from core.loader import logger


class LoggingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.logger = logger
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update, 
        data: Dict[str, Any]
    ) -> Coroutine[Any, Any, Any]:
        
        if event.message:
            message: Message = event.message
            logger.info(f"Processing: id[{message.from_user.id}] : msg[{message.text}]")

        return await handler(event, data)

