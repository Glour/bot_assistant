from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from utils.working_with_dialogs import Document

doc = Document()


async def reset_context(msg: Message):
    file_path = f'dialogs/dialog{msg.from_user.id}.json'
    messages = doc.read_messages_from_file(file_path)
    # сохраняем весь текущий диалог
    save_file_path = f'old_dialogs/old_dialog{msg.from_user.id}.json'
    doc.save_old_messages_to_file(save_file_path, messages)
    # оставляем текущий диалог пустым
    doc.save_messages_to_file(file_path, [])
    await msg.answer('История сообщений отчищена\nНачало нового диалога')


def register_reset_messages(dp: Dispatcher):
    dp.register_message_handler(reset_context, Command('reset_context'), state="*")
