import os
from telebot import TeleBot
from telebot import types
from dotenv import load_dotenv
from get_intent_text import detect_intent_texts
from bot_logging import TelegramLogsHandler
import logging

logger = logging.getLogger()


class TelegramBot:
    def __init__(self, BOT_TOKEN, PROJECT_ID):
        self.bot = TeleBot(token=BOT_TOKEN)
        logger.info('Tg bot started!')

        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            bot_command = types.BotCommand('start', 'Стартовая страница')
            command_scope = types.BotCommandScopeChat(message.chat.id)
            self.bot.set_my_commands([bot_command], command_scope)
            self.bot.send_message(message.chat.id, text='Привет!')

        @self.bot.message_handler(content_types=["text"])
        def repeat_all_messages(message):
            answer = detect_intent_texts(
                PROJECT_ID,
                session_id=message.chat.id,
                texts=message.text,
                language_code='ru-RU'
            ).fulfillment_text
            self.bot.send_message(message.chat.id, answer)

        self.bot.infinity_polling()


def main():
    load_dotenv()
    chat_id = os.getenv("TG_CHAT_ID")
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    bot_token = os.getenv("TG_BOT_TOKEN")
    bot = TeleBot(token=bot_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))

    try:
        TelegramBot(bot_token, project_id)

    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
