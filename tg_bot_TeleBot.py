import os

from telebot import TeleBot
from dotenv import load_dotenv
from get_intent_text import detect_intent_texts
from bot_logging import TelegramLogsHandler
import logging

logger = logging.getLogger()

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot

    def handle(self):
        @self.bot.message_handler(commands=['start'])
        def handle(msg) -> None:
            if msg.text == '/start':
                self.bot.send_message(msg.chat.id, 'Привет!')


class TextHandler:
    def __init__(self, bot, project_id):
        self.bot = bot
        self.project_id = project_id

    def handle(self):
        @self.bot.message_handler(content_types=["text"])
        def text_handle(msg) -> None:
            answer = detect_intent_texts(
                self.project_id,
                session_id=msg.chat.id,
                texts=msg.text,
                language_code='ru-RU'
            ).fulfillment_text
            self.bot.send_message(msg.chat.id, answer)


class MainHandler:
    def __init__(self, bot, project_id):
        self._bot = bot
        self.project_id = project_id
        self._com_handler = CommandHandler(self._bot)
        self._text_handler = TextHandler(self._bot, self.project_id)

    def handle(self) -> None:
        self._com_handler.handle()
        self._text_handler.handle()


class TelegramBot:

    def __init__(self, bot, project_id):
        self._bot = bot
        self.project_id = project_id
        self._handler = MainHandler(self._bot, self.project_id)
        self._t_handler = MainHandler(self._bot, self.project_id)

    def _start(self) -> None:
        self._handler.handle()

    def run(self) -> None:
        self._start()
        self._bot.polling(non_stop=True)


def main():
    load_dotenv()
    chat_id = os.getenv("TG_CHAT_ID")
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    bot_token = os.getenv("TG_BOT_TOKEN")
    bot = TeleBot(token=bot_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))

    try:
        bot = TelegramBot(bot, project_id)
        logger.info('TG_bot started')
        bot.run()

    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
