import json
from typing import Any

import backoff as backoff
import openai

from settings import config
from utils.logger import logger

openai.api_key = config.openai_api_key


def read_messages_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            messages = json.load(file)
    except json.JSONDecodeError:
        messages = []
    return messages


def save_messages_to_file(file_path, messages):
    with open(file_path, "w") as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
@backoff.on_exception(backoff.expo, openai.error.OpenAIError)
@backoff.on_exception(backoff.expo, openai.error.APIError)
async def create_chat_completion(msg) -> Any | None:
    file_path = f'dialogs/dialog{msg.from_user.id}.json'
    messages = read_messages_from_file(file_path)  # проверяем наличие непустого диалога
    messages.append({"role": "user", "content": msg.text})  # записываем вопрос в диалог

    try:
        completion = await openai.ChatCompletion.acreate(
            messages=messages,
            model='gpt-3.5-turbo',
            max_tokens=700,
            temperature=0.6
        )
        chat_response = completion.choices[0]['message']['content']
        messages.append({"role": "assistant", "content": chat_response})  # записываем ответ в диалог
        save_messages_to_file(file_path, messages)  # сохраняем диалог в файл
        return chat_response

    # Обработка ошибок API
    except openai.error.InvalidRequestError as e:  # обработка ошибки превышение лимита контекста
        with open(file_path, "r+") as file:
            messages = json.load(file)
            file.seek(0)
            json.dump(messages[:-7], file)  # обрезаем начало диалога
            file.truncate()
        return await create_chat_completion(msg)  # генерируем ответ снова без прерывания диалога для пользователя

    except Exception as e:
        logger.error(f'произошла ошибка {e}')
        return None
