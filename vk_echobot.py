import random, os
from dotenv import load_dotenv
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters
)
from dialog_operations import detect_intent_texts, dialogflow


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(f'Hi {user.username}, i\'am bot speaker!')


def bot_answer(update: Update, context: CallbackContext):
    message_text = [update.message.text]
    answer_text = detect_intent_texts(
                        os.environ.get('PROJECT_ID'),
                        update.effective_user,
                        message_text
    )
    update.message.reply_text(answer_text)
    print(f'message {message_text}')
    print(f'answer {answer_text}')


def detect_intent_texts(project_id, session_id, texts, language_code='ru'):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        if response.query_result.intent.is_fallback:
            return
        else:
            return response.query_result.fulfillment_text


def echo(event, vk_api, client_id, project_id):
    answer_text = detect_intent_texts(
                        project_id,
                        client_id,
                        [event.text],
    )
    if not answer_text is None:
        vk_api.messages.send(
            user_id=event.user_id,
            message=f'{answer_text}',
            random_id=random.randint(1,1000)
        )


def main():
    load_dotenv()
    vk_token = os.environ.get('VK_KEY')
    bot_token = os.environ.get('BOT_TOKEN')
    project_id = os.environ.get('PROJECT_ID')

    # updater = Updater(bot_token)
    # dispatcher = updater.dispatcher
    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, bot_answer))
    # updater.start_polling()
    # updater.idle()

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, vk_session.client_secret, project_id)


if __name__ == '__main__':
    main()
