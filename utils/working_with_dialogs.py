import json


class Document:

    @staticmethod
    def read_messages_from_file(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                messages = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            messages = []
        return messages

    @staticmethod
    def save_messages_to_file(file_path, messages):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(messages, file, indent=4, ensure_ascii=False)

    def cut_the_dialog(self, file_path):
        messages = self.read_messages_from_file(file_path)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(messages[1:], file, indent=4, ensure_ascii=False)  # обрезаем начало диалога
            return [messages[0]]

    def save_old_messages_to_file(self, file_path, old_messages):
        if len(old_messages) > 0:
            all_messages = self.read_messages_from_file(file_path)
            self.save_messages_to_file(file_path, all_messages + old_messages)
