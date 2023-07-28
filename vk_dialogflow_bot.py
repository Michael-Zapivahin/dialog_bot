import random
import os
import vk_api as vk
import logging
import telebot

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from logging.handlers import RotatingFileHandler
from requests.exceptions import HTTPError

from dialog_operations import detect_intent_texts
from logger import TelegramLogsHandler


logger = logging.getLogger(__name__)


def get_question_answer(event, vk_api, client_id, project_id):
    answer_text = detect_intent_texts(
                        project_id,
                        client_id,
                        [event.text],
    )
    if answer_text is not None:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer_text,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()
    vk_token = os.environ.get('VK_KEY')
    project_id = os.environ.get('PROJECT_ID')
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

    logger.info('The VK bot started!')

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                get_question_answer(event, vk_api, vk_session.client_secret, project_id)
            except HTTPError or ConnectionError as error:
                logger.error(f'Network error: {error}')
            except Exception as error:
                logger.exception(f'The bot stopped with error: {error}')


if __name__ == '__main__':
    main()
