import json
import os

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message


async def user_start(msg: Message):
    await msg.answer('Привет! Я бот, готовый отвечать на ваши вопросы. Просто задайте мне вопрос, и я постараюсь '
                     'предоставить вам наиболее полезную информацию')
    # создаем новый файл если еще не создан для записи диалога пользователя
    if not os.path.exists(f'dialogs/dialog{msg.from_user.id}.json'):
        with open(f'dialogs/dialog{msg.from_user.id}.json', "w") as file:
            json.dump([], file)


def register_start_user(dp: Dispatcher):
    dp.register_message_handler(user_start, CommandStart(), state="*")
