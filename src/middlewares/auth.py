from typing import Any, Awaitable, Callable, Dict, Optional
import json

from aiogram import BaseMiddleware, types
from aiogram.types import Message, TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from core import redis_client, logger
from core.exceptions import DBSessionMiddlewareError
from models.user import User
from services.user import fetch_user


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            data["user"] = None
            return await handler(event, data)

        try:
            session: AsyncSession = data["session"]
        except KeyError:
            raise DBSessionMiddlewareError()

        # fetch user and attach his db data to event data
        message: Message = event
        tg_user: types.User = message.from_user
        db_user: Optional[User] = await fetch_user(tg_user.id, session)

        if db_user is None:
            data["user"] = None
            return await handler(event, data)

        # merge user to current db session
        db_user = await session.merge(db_user)

        data["user"] = db_user
        return await handler(event, data)
