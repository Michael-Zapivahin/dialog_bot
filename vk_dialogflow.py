import random
import os
import vk_api as vk

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_operations import detect_intent_texts


def echo(event, vk_api, client_id, project_id):
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

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, vk_session.client_secret, project_id)


if __name__ == '__main__':
    main()
