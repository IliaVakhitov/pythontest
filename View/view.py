import logging


def print_str(message) -> None:
    print(message)


def input_str(message) -> str:
    read_str = input(message)
    logging.info("User input {}".format(read_str))
    if read_str == "exit()":
        logging.info("User exit")
        exit()
    return read_str


def input_user_answer(message="") -> int:
    read_str = input_str(message)
    try:
        index = int(read_str)
    except:
        index = -1
    if index < 1 or index > 4:
        input_user_answer("Please, select from 1 to 4!")

    return index
