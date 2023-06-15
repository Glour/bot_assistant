import os

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.json import json


async def reset_context(msg: Message):
    await msg.answer('История сообщений отчищена\nНачало нового диалога')
    with open(f'dialogs/dialog{msg.from_user.id}.json', "w") as file:
        json.dump([], file)


def register_reset_messages(dp: Dispatcher):
    dp.register_message_handler(reset_context, Command('reset_context'), state="*")
