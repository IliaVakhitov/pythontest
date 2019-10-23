from View import view
from Model.Dictionary import Dictionary
import os

my_dictionaries = []


def load_dictionaries():
    for file in os.listdir("Dictionaries"):
        if file.endswith(".json"):
            my_dict = Dictionary("")
            my_dict.read_from_json(os.path.join("Dictionaries", file))
            my_dictionaries.append(my_dict)


def print_dictionaries():
    for my_dict in my_dictionaries:
        view.print_str(my_dict.print_information())


def generate_game(words_number):
    pass


class Model:
    pass
