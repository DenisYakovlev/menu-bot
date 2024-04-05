from aiogram import Dispatcher

from .db_session import DBSessionMiddleware
from .logging import LoggingMiddleware
from .auth import AuthMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(LoggingMiddleware())
    dp.update.outer_middleware(DBSessionMiddleware())
    dp.message.outer_middleware(AuthMiddleware())
