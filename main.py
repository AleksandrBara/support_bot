import os
from telebot import TeleBot
from telebot import types
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")
PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')

bot = TeleBot(token=BOT_TOKEN)


def detect_intent_texts(project_id, session_id, texts, language_code):
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


@bot.message_handler(commands=['start'])
def start_message(message):
    bot_command = types.BotCommand('start', 'Стартовая страница')
    command_scope = types.BotCommandScopeChat(message.chat.id)
    bot.set_my_commands([bot_command], command_scope)
    bot.send_message(message.chat.id, text='Привет!')


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    answer = detect_intent_texts(
        PROJECT_ID,
        session_id=message.chat.id,
        texts=message.text,
        language_code='ru-RU'
    )
    bot.send_message(message.chat.id, answer)


if __name__ == '__main__':
    bot.infinity_polling()
