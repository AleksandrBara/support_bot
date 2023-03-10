import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import os
import random
from get_intent_text import detect_intent_texts
from bot_logging import TelegramLogsHandler
from telebot import TeleBot
import logging

logger = logging.getLogger()


def answer_to_user(event, vk_api):
    answer = detect_intent_texts(
        project_id,
        session_id,
        event.text,
        language_code='ru-RU'
    )

    if answer.intent.is_fallback:
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=answer.fulfillment_text,
        random_id=random.randint(1, 1000)
    )


def bot_srart():
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer_to_user(event, vk_api)


if __name__ == "__main__":
    load_dotenv()
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_id = os.getenv('DIALOGFLOW_SESSION_ID')
    vk_group_token = os.getenv('VK_KEY')
    bot_token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")

    log_bot = TeleBot(token=bot_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))

    try:
        bot_srart()
        logger.info('VK bot started!')
    except Exception as e:
        logger.exception(e)
