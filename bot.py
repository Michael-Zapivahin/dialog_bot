
import os

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters
)
from dotenv import load_dotenv
from google.cloud import dialogflow



def detect_intent_texts(project_id, session_id, texts, language_code='ru'):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    # print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        return response.query_result.fulfillment_text


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


def detect_intent_texts(project_id, session_id, texts, language_code='ru'):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    # print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        return response.query_result.fulfillment_text


def main():
    load_dotenv()
    token = os.environ.get('BOT_TOKEN')

    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, bot_answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
