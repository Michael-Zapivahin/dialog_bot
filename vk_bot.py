
import os, random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dotenv import load_dotenv

from bot import detect_intent_texts


def send_answer(project_id, text, user_id):

    answer = detect_intent_texts(
                        project_id=project_id,
                        session_id=user_id,
                        texts=[text]
    )
    print(text, answer)



def main():
    load_dotenv()
    token = os.environ.get('VK_KEY')
    project_id = os.environ.get('PROJECT_ID')
    vk_session = vk.VkApi(token=token)
    long_poll = VkLongPoll(vk_session)
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            send_answer(project_id=project_id, text=event.text, user_id=event.user_id)


if __name__ == '__main__':
    main()

