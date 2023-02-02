import os
from telebot import TeleBot
from telebot import types
from dotenv import load_dotenv
from secondary_func import (
    detect_intent_texts,
    TelegramLogsHandler
)
import logging


def bot_start():
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot_command = types.BotCommand('start', 'Стартовая страница')
        command_scope = types.BotCommandScopeChat(message.chat.id)
        bot.set_my_commands([bot_command], command_scope)
        bot.send_message(message.chat.id, text='Привет!')

    @bot.message_handler(content_types=["text"])
    def repeat_all_messages(message):
        answer = detect_intent_texts(
            project_id,
            session_id=message.chat.id,
            texts=message.text,
            language_code='ru-RU'
        ).fulfillment_text
        bot.send_message(message.chat.id, answer)

    bot.infinity_polling()


if __name__ == '__main__':
    load_dotenv()
    bot_token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')

    bot = TeleBot(token=bot_token)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logging.info('Tg bot started!')

    try:
        bot_start()
    except Exception as e:
        logging.exception(e)
