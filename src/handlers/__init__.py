from aiogram import Router

from . import (
    start,
    test,
    settings,
    core,
    menu,
    menu_settings,
    menu_create,
    meal_create,
    menu_edit,
    menu_choose,
    orders,
    payment
)

def get_handlers_router() -> Router:
    router = Router()

    router.include_router(start.router)
    router.include_router(test.router)
    router.include_router(settings.router)
    router.include_router(core.router)
    router.include_router(menu.router)
    router.include_router(menu_settings.router)
    router.include_router(menu_create.router)
    router.include_router(meal_create.router)
    router.include_router(menu_edit.router)
    router.include_router(menu_choose.router)
    router.include_router(orders.router)
    router.include_router(payment.router)

    return router
