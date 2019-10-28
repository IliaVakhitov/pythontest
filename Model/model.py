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


def get_random_translation(all_words, word):
    new_word = all_words[random.randint(0, len(all_words)-1)]
    while new_word.translation == word.translation:
        new_word = all_words[random.randint(0, len(all_words) - 1)]

    return new_word.translation


def generate_game(words_number = 0):
    all_words = []
    game_rounds = []
    for next_dictionary in my_dictionaries:
        all_words += next_dictionary.words

    all_words = mix_list(all_words)
    for next_word in all_words:
        translations = [next_word.translation]
        for i in range(3):
            translations.append(get_random_translation(all_words, next_word))
        translations = mix_list(translations)
        correct_index = -1
        for str in translations:
            if str == next_word.translation:
                correct_index = translations.index(str)
        if correct_index == -1:
            # TODO error in correct index
            correct_index = 1
        game_rounds.append(
            GameRound(
                next_word.word,
                translations,
                next_word.translation,
                correct_index
            ))

    return game_rounds


def mix_list(my_list):
    list_length = len(my_list) - 1
    tmp_list = my_list.copy()
    new_list = []
    for i in range(list_length + 1):
        new_list.append(
            tmp_list.pop(
                random.randint(0, len(tmp_list)-1)))

    return new_list


class GameRound:
    def __init__(self, word, translations, correct_answer, correct_index):
        self.word = word
        self.translation1 = translations[0]
        self.translation2 = translations[1]
        self.translation3 = translations[2]
        self.translation4 = translations[3]
        self.correct_answer = correct_answer
        self.correct_index = correct_index

    def is_answer_correct(self, answer):
        return answer == self.correct_answer

    def is_index_correct(self, index):
        return index == self.correct_index

    def print_game_round(self):
        return_str = self.word + "\n"
        return_str += self.translation1 + " "
        return_str += self.translation2 + " "
        return_str += self.translation3 + " "
        return_str += self.translation4 + "\n"
        return_str += "Correct {} - {} ".format(self.correct_answer, self.correct_index)
        return return_str


class Model:
    pass


