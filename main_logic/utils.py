import urllib.request
import random
from main_logic.models import (
    Question
)
from docx import Document


def handle_uploaded_file(file):
    doc = Document(file)
    questions = {}
    count = 0

    for paragraph in doc.paragraphs:
        line = paragraph.text.strip()

        if not line:  # Skip empty lines
            continue

        if line.startswith('#'):
            count += 1
            questions["question_" +
                      str(count)] = [{"text": line[1:], "is_correct": False}]
        elif line.startswith('$') or line.startswith('&'):
            if count == 0:
                raise ValueError("Option or answer found before any question!")
            is_correct = line.startswith('&')
            questions["question_" +
                      str(count)].append({"text": line[1:], "is_correct": is_correct})

    return questions


def check_users_achievenment(user):

    return


def get_random_ids(count: int, obj: object) -> list:
    all_ids = obj.values_list('id', flat=True)
    print(all_ids)
    if len(all_ids) < count:
        return all_ids
    else:
        return random.sample(list(all_ids), count)
