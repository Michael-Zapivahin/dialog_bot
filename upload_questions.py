import os
import json

from dotenv import load_dotenv
from dialog_operations import create_intent


def main():

    load_dotenv()
    project_id = os.environ.get('PROJECT_ID')
    with open(os.path.join('dictionaries', 'questions.json'), "r") as my_file:
        questions_json = my_file.read()

    questions = json.loads(questions_json)

    for intent_name in questions.keys():
        intent = questions[intent_name]
        create_intent(
            project_id,
            intent_name,
            intent['questions'],
            [intent['answer']],
        )


if __name__ == '__main__':
    main()
