import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import os
import random
from main import detect_intent_texts


PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
SESSION_ID = os.getenv('DIALOGFLOW_SESSION_ID')

def echo(event, vk_api):

    answer = detect_intent_texts(
        PROJECT_ID,
        SESSION_ID,
        event.text,
        language_code='ru-RU'
    )
    print(answer.intent.is_fallback)
    if answer.intent.is_fallback:
        return
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer.fulfillment_text,
        random_id=random.randint(1,1000)
    )

if __name__ == "__main__":
    load_dotenv()
    vk_group_token = os.getenv('VK_KEY')
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)

