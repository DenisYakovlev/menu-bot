from aiogram import Dispatcher

from .logging import LoggingMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(LoggingMiddleware())
