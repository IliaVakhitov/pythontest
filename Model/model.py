from View import view
from Model.Dictionary import Dictionary
from Model.Dictionary import DictionaryLoaderJson
import os
import random

my_dictionaries = []


def load_dictionaries():
    dictionaryloader = DictionaryLoaderJson()
    for file in os.listdir("Dictionaries"):
        if file.endswith(".json"):
            my_dict = Dictionary("")
            dictionaryloader.filename = os.path.join("Dictionaries", file)
            if dictionaryloader.load_dictionary(my_dict):
                my_dictionaries.append(my_dict)


def print_dictionaries():
    for my_dict in my_dictionaries:
        view.print_str(my_dict.print_information())


def generate_game(words_number):
    pass


def mix_list(my_list):
    list_length = len(my_list) - 1
    indexes = []
    for i in range(list_length + 1):
        added = False
        while not added:
            new_index = random.randint(0, list_length)
            if new_index not in indexes:
                indexes.append(new_index)
                added = True

    new_list = []
    for i in indexes:
        new_list.append(my_list[i])

    return new_list


class GameRound:
    def __init__(self, word, translation1, translation2, translation3, translation4, correct_answer, correct_index):
        self.word = word
        self.translation1 = translation1
        self.translation2 = translation2
        self.translation3 = translation3
        self.translation4 = translation4
        self.correct_answer = correct_answer
        self.correct_index = correct_index

    def is_answer_correct(self, answer):
        return answer == self.correct_answer

    def is_index_correct(self, index):
        return index == self.correct_index


class Model:
    pass


