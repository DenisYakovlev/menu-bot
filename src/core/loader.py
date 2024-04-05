import logging.config

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from redis.asyncio import Redis

from cache.connection import redis_pool
from core.config import settings

# init logger
logging.config.dictConfig(settings.LOGGING_CONFIG)

logger = logging.getLogger("default")

# init bot
bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)

# init redis
redis_pool.init(settings.CACHE)

redis_client = Redis(connection_pool=redis_pool.pool)

# init storage
storage = RedisStorage(
    redis=redis_client,
    key_builder=DefaultKeyBuilder(with_bot_id=True),
)

# init dispatcher
dp = Dispatcher(storage=storage)
