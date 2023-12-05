import string
import random
import datetime


def generate_random_sequence(length=20):
    characters = string.ascii_letters + string.digits + "-_"
    random_sequence = ''.join(random.choice(characters) for _ in range(length))
    return random_sequence


def get_today():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_datetime