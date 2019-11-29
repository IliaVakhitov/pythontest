import logging
import re
from getpass import getpass


def print_str(message) -> None:

    print(message)


def input_str(message) -> str:

    read_str = input(message)
    logging.info(f"User input \'{read_str}\'")
    if read_str == "exit()":
        logging.info("User exit")
        exit()
    return read_str


def input_user_choice(message: str = "", regex: str = "") -> int:

    while True:
        user_input = input_str(message)
        if re.match(regex, user_input):
            break
    return int(user_input)


def input_user_answer(message: str = "") -> int:

    while True:
        user_input = input_str(message)
        if re.match("[1-4](?!\\d)", user_input):
            break
    return int(user_input)


def input_password(message: str = "") -> str:

    print(message)
    return getpass()
