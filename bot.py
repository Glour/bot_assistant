import asyncio

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.generate_answer import register_answer_user
from handlers.new_dialog import register_reset_messages
from handlers.start import register_start_user
from middlewares.throttling import ThrottlingMiddleware
from settings import config
from utils.logger import logger
from utils.set_bot_commands import set_default_commands


def register_all_middlewares(dp):
    dp.setup_middleware(ThrottlingMiddleware())


def register_all_handlers(dp):
    register_start_user(dp)
    register_reset_messages(dp)
    register_answer_user(dp)


async def main():
    logger.info("Starting bot")

    storage = MemoryStorage()

    bot = Bot(token=config.bot_token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    register_all_middlewares(dp)
    register_all_handlers(dp)
    await set_default_commands(dp)
    # start
    try:
        await dp.start_polling()

    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
