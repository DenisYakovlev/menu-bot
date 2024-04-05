from aiogram import Router

from . import start
from . import test
from . import settings
from . import core
from . import menu
from . import menu_settings

def get_handlers_router() -> Router:
    router = Router()

    router.include_router(start.router)
    router.include_router(test.router)
    router.include_router(settings.router)
    router.include_router(core.router)
    router.include_router(menu.router)
    router.include_router(menu_settings.router)

    return router
