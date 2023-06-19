from typing import Any

import backoff
import openai

from settings import config
from utils.logger import logger

openai.api_key = config.openai_api_key


class ChatBot:

    @backoff.on_exception(backoff.expo, (openai.error.RateLimitError, openai.error.APIError, openai.error.OpenAIError))
    async def create_chat_completion(self, msg: Any, doc) -> Any | None:
        file_path = f'dialogs/dialog{msg.from_user.id}.json'
        messages = doc.read_messages_from_file(file_path)  # проверяем наличие непустого диалога
        messages.append({"role": "user", "content": f"{msg.text}"})  # записываем вопрос в диалог
        # запускаем асинхронную генерацию ответа с нашими параметрами
        try:
            completion = await openai.ChatCompletion.acreate(
                messages=messages,
                model='gpt-3.5-turbo',
                max_tokens=700,
                temperature=0.6
            )
            chat_response = completion.choices[0]['message']['content']
            messages.append({"role": "assistant", "content": chat_response})  # записываем ответ в диалог
            doc.save_messages_to_file(file_path, messages)  # сохраняем диалог в файл
            return chat_response
        # обработка ошибки превышение лимита контекста
        except openai.error.InvalidRequestError as e:
            cut_message = doc.cut_the_dialog(file_path)
            save_file_path = f'old_dialogs/old_dialog{msg.from_user.id}.json'
            doc.save_old_messages_to_file(save_file_path, cut_message)
            # генерируем ответ снова без прерывания диалога для пользователя
            return await self.create_chat_completion(msg, doc)

        except Exception as e:
            logger.error(f'произошла ошибка {e}')
            return None
