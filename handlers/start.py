from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message


async def user_start(msg: Message):
    await msg.answer('Привет! Я бот, готовый отвечать на ваши вопросы. Просто задайте мне вопрос, и я постараюсь '
                     'предоставить вам наиболее полезную информацию')


def register_start_user(dp: Dispatcher):
    dp.register_message_handler(user_start, CommandStart(), state="*")
