import asyncio

from core.loader import bot, dp, logger
from db.session import sessionmanager
from handlers import get_handlers_router
from middlewares import register_middlewares


async def on_startup() -> None:
    logger.info("starting...")

    # manage middlewares
    register_middlewares(dp)

    # manage routers
    dp.include_router(get_handlers_router())

    # log bot info
    bot_info = await bot.get_me()

    logger.info(f"Name     - {bot_info.full_name}")
    logger.info(f"Username - @{bot_info.username}")
    logger.info(f"ID       - {bot_info.id}")

    states: dict[bool | None, str] = {
        True: "Enabled",
        False: "Disabled",
        None: "Unknown (This's not a bot)",
    }

    logger.info(f"Groups Mode  - {states[bot_info.can_join_groups]}")
    logger.info(
        f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logger.info(f"Inline Mode  - {states[bot_info.supports_inline_queries]}")

    logger.info("bot started")


async def on_shutdown() -> None:
    logger.info("shutting down...")

    # close db session
    await sessionmanager.close()

    # close redis session
    await dp.storage.close()

    # close bot session
    await bot.session.close()

    logger.info("bot stopped")


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


asyncio.run(main())
