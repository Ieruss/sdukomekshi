import asyncio
import logging
import sys
import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage, Redis

from loader import config, db
from arq import create_pool
from arq.connections import RedisSettings

redis = Redis(host='localhost', port=6380)
key_builder = DefaultKeyBuilder(with_destiny=True)


async def setup_aiogram(dispatcher: Dispatcher) -> None:
    from handlers import setup_routers
    from middlewares.update import UpdateUserMiddleware
    from middlewares.throttling import ThrottlingMiddleware
    from middlewares.permission import PermissionMiddleware
    from middlewares.auth_check import AuthCheckerMiddleware
    dispatcher.include_router(setup_routers())
    dispatcher.update.middleware(ThrottlingMiddleware(redis=redis))
    dispatcher.update.middleware(UpdateUserMiddleware(db))
    dispatcher.message.middleware(PermissionMiddleware(db))
    dispatcher.message.middleware(AuthCheckerMiddleware(db))


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    from utils.notify_admin import on_startup_notify
    from utils.set_bot_commands import set_default_commands

    logger.info("Starting polling")
    await db.create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher=dispatcher)
    await on_startup_notify(bot=bot, ADMINS=config.admins.list)
    await set_default_commands(bot=bot)


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot):
    logger.info("Stopping polling")
    await bot.session.close()
    await dispatcher.storage.close()


async def main() -> None:
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = RedisStorage(redis=redis, key_builder=key_builder)
    redis_pool = await create_pool(RedisSettings(host='localhost', port=6380))
    dp = Dispatcher(storage=storage)
    dp.startup.register(aiogram_on_startup_polling)
    dp.shutdown.register(aiogram_on_shutdown_polling)
    await dp.start_polling(bot, db=db, arqredis=redis_pool)


if __name__ == "__main__":
    bl.basic_colorized_config(level=logging.INFO)
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped!")
