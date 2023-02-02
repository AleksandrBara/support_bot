import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import os
import random
from secondary_func import (
    detect_intent_texts,
    TelegramLogsHandler
)
from telebot import TeleBot
import logging


def echo(event, vk_api):
    answer = detect_intent_texts(
        project_id,
        session_id,
        event.text,
        language_code='ru-RU'
    )
    print(answer.intent.is_fallback)
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
            echo(event, vk_api)


if __name__ == "__main__":
    load_dotenv()
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_id = os.getenv('DIALOGFLOW_SESSION_ID')
    vk_group_token = os.getenv('VK_KEY')
    bot_token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")

    log_bot = TeleBot(token=bot_token)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))
    logging.info('VK bot started!')

    try:
        bot_srart()
    except Exception as e:
        logging.exception(e)
