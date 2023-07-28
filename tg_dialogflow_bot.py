
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
from dialog_operations import detect_intent_texts
from logging.handlers import RotatingFileHandler
from requests.exceptions import HTTPError

from logger import TelegramLogsHandler


logger = logging.getLogger(__name__)


def processing_errors(bot, update, telegram_error):
    logger.error(f'telegram error: {telegram_error}')


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(f'Hi {user.username}, i\'am bot speaker!')


def bot_answer(update: Update, context: CallbackContext):
    message_text = [update.message.text]
    answer = detect_intent_texts(
                        os.environ.get('PROJECT_ID'),
                        update.effective_user,
                        message_text
    )
    update.message.reply_text(answer.fulfillment_text)


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
    dispatcher.add_error_handler(processing_errors)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
