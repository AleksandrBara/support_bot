import os
from telebot import TeleBot
from telebot import types
from dotenv import load_dotenv
from get_intent_text import detect_intent_texts
from bot_logging import TelegramLogsHandler
import logging

logger = logging.getLogger()

load_dotenv()

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
BOT = TeleBot(token=BOT_TOKEN)


def bot_start(project_id):
    @BOT.message_handler(commands=['start'])
    def start_message(message):
        bot_command = types.BotCommand('start', 'Стартовая страница')
        command_scope = types.BotCommandScopeChat(message.chat.id)
        BOT.set_my_commands([bot_command], command_scope)
        BOT.send_message(message.chat.id, text='Привет!')

    @BOT.message_handler(content_types=["text"])
    def repeat_all_messages(message):
        answer = detect_intent_texts(
            project_id,
            session_id=message.chat.id,
            texts=message.text,
            language_code='ru-RU'
        ).fulfillment_text
        BOT.send_message(message.chat.id, answer)


def main():
    chat_id = os.getenv("TG_CHAT_ID")
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(BOT, chat_id))

    try:
        bot_start(project_id)
        logger.info('Tg bot started!')
    except Exception as e:
        logger.exception(e)

    BOT.infinity_polling()


if __name__ == '__main__':
    main()

