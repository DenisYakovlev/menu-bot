from aiogram import Router

from . import start, test, redis_test


def get_handlers_router() -> Router:
    router = Router()

    router.include_router(start.router)
    router.include_router(test.router)
    router.include_router(redis_test.router)

    return router
