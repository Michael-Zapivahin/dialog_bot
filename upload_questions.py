import os
import json
import argparse

import google.api_core.exceptions
from dotenv import load_dotenv
from dialog_operations import create_intent


def main():
    parser = argparse.ArgumentParser(description='Script download books')
    parser.add_argument('--questions_path', help='JSON file path', type=str, default='questions.json')
    args = parser.parse_args()
    questions_path = args.questions_path

    load_dotenv()
    project_id = os.environ.get('PROJECT_ID')
    with open(questions_path, "r") as file:
        questions_json = file.read()

    questions = json.loads(questions_json)
    for question_name, question in questions.items():
        try:
            create_intent(
                project_id,
                question_name,
                question['questions'],
                question['answer'],
            )
        except google.api_core.exceptions.InvalidArgument:
            print(f'Intent with the display name "{question_name}" already exists.')


if __name__ == '__main__':
    main()
