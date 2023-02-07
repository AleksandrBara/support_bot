import os
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Filters, Updater, CommandHandler, MessageHandler, CallbackContext
import logging
from get_intent_text import detect_intent_texts
from telegram import Bot

logger = logging.getLogger()


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.chat_id, log_entry)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет!')


def answer_to_user(update: Update, context: CallbackContext) -> None:
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_id = os.getenv('DIALOGFLOW_SESSION_ID')
    answer = detect_intent_texts(
        project_id,
        session_id,
        update.message.text,
        'ru-RU'
    ).fulfillment_text
    update.message.reply_text(answer)


def run_bot(token) -> None:
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, answer_to_user)
    )

    updater.start_polling()

    updater.idle()


def main() -> None:
    load_dotenv()
    chat_id = os.getenv("TG_CHAT_ID")
    bot_token = os.getenv("TG_BOT_TOKEN")

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot_token, chat_id))

    try:
        run_bot(bot_token)
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
