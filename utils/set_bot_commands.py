from aiogram.types import BotCommand


async def set_default_commands(dp):
    return await dp.bot.set_my_commands(
        [
            BotCommand("start", "Запустить бота"),
            BotCommand("reset_context", "Начать новый диалог")
        ]
    )

