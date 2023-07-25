
import os
import logging
import telebot

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters
)
from dotenv import load_dotenv
from dialog_operations import detect_intent_texts, dialogflow
from logging.handlers import RotatingFileHandler
from requests.exceptions import HTTPError


logger = logging.getLogger(__name__)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(f'Hi {user.username}, i\'am bot speaker!')


def bot_answer(update: Update, context: CallbackContext):
    try:
        message_text = [update.message.text]
        answer_text = detect_intent_texts(
                            os.environ.get('PROJECT_ID'),
                            update.effective_user,
                            message_text
        )
        update.message.reply_text(answer_text)
    except HTTPError or ConnectionError as error:
        logger.error(f'Network error: {error}')
    except Exception as error:
        logger.exception(f'The bot stopped with error: {error}')


def detect_intent_texts(project_id, session_id, texts, language_code='ru'):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

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
    chat_log_id = os.environ['TG_CHAT_ID']

    bot = telebot.TeleBot(token)

    file_handler = RotatingFileHandler('bot.log', maxBytes=200000, backupCount=2)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    telegram_handler = TelegramLogsHandler(bot, chat_log_id)
    telegram_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(telegram_handler)

    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    logger.info('The dialogflow bot started!')

    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, bot_answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
