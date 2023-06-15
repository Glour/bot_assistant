import asyncio

from aiogram import Dispatcher
from aiogram.types import Message

from utils.engine import create_chat_completion


async def show_generation_status(wait_message: Message):
    frame_index = 0
    animation_frames = [
        '⠀\nРежим непонятки...🤔  \n⠀',
        '⠀\nАнализирую данные🔎\n⠀',
        '⠀\nГенерирую текст... 💡   \n⠀',
    ]
    while True:
        await asyncio.sleep(0.6)
        await wait_message.edit_text(animation_frames[frame_index])
        frame_index = (frame_index + 1) % len(animation_frames)


async def generate_answer(msg: Message):
    wait_message = await msg.answer("⠀\n✅ Запрос отправлен\n⠀")
    show_generation_task = asyncio.create_task(show_generation_status(wait_message))
    result = await create_chat_completion(msg)
    if result:
        await msg.answer(result)
    else:
        pass
        # await msg.answer('Сервер не смог обработать ваш запрос\nПовторите еще раз, либо попробуйте изменить его.')
    show_generation_task.cancel()
    await wait_message.delete()


def register_answer_user(dp: Dispatcher):
    dp.register_message_handler(generate_answer, content_types=['text'], state="*")
