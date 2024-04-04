from aiogram import Dispatcher

from .db_session import DBSessionMiddleware
from .logging import LoggingMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(LoggingMiddleware())
    dp.update.outer_middleware(DBSessionMiddleware())
