from View import view
from Model.Dictionary import Dictionary
from Model.Dictionary import DictionaryLoaderJson
import os
import random
import logging

my_dictionaries = []


def load_dictionaries():
    logging.info("Loading dictionaries.")
    dictionaryloader = DictionaryLoaderJson()
    for file in os.listdir("Dictionaries"):
        if file.endswith(".json"):
            logging.info("Start reading file {}".format(os.path.join("Dictionaries", file)))
            my_dict = Dictionary("")
            dictionaryloader.filename = os.path.join("Dictionaries", file)
            if dictionaryloader.load_dictionary(my_dict):
                logging.info("Dictionary {} added".format(my_dict.name))
                logging.info("Total words {} ".format(len(my_dict.words)))
                my_dictionaries.append(my_dict)
    logging.info("Total dictionaries loaded {}".format(len(my_dictionaries)))


def print_dictionaries():
    for my_dict in my_dictionaries:
        view.print_str(my_dict.print_information())


def get_random_translation(all_words, translation, translations):
    new_word = all_words[random.randint(0, len(all_words) - 1)]
    while (new_word.translation == translation) or (new_word.translation in translations):
        new_word = all_words[random.randint(0, len(all_words) - 1)]

    return new_word.translation


def play_game(game_rounds):
    view.print_str("Game starts!")
    view.print_str("Print exit() for exit")
    logging.info("New game started")
    correct_answers = 0
    incorrect_answers = 0
    for game_round in game_rounds:
        view.print_str(game_round.print_game_round())
        logging.info("Word {} correct answer {}".format(game_round.word, game_round.correct_index))
        index = view.input_user_answer("Please, choose correct word:")
        logging.info("User answer {} is {}".format(
            index,
            "correct" if index == game_round.correct_index else "incorrect"))
        if index == game_round.correct_index:
            correct_answers += 1
            # view.print_str("Correct!")
        else:
            incorrect_answers += 1
            # view.print_str("InCorrect!")
    logging.info("Game ended. Correct answers {}. Incorrect answers {}". format(correct_answers, incorrect_answers))


def generate_game(words_number=0):
    """
    Generates list of GameRounds
    return
    None - if no words is dictionaries
    List of GameRounds:
    """
    all_words = []
    game_rounds = []
    for next_dictionary in my_dictionaries:
        all_words += next_dictionary.words
    if len(all_words) == 0:
        # No words in dictionaries
        return None

    all_words = mix_list(all_words)
    for next_word in all_words:
        if 0 < words_number <= len(game_rounds):
            break
        correct_index = random.randint(0, 3)
        translations = []
        for i in range(3):
            translations.append(get_random_translation(all_words, next_word.translation, translations))
        translations.insert(correct_index, next_word.translation)
        # New game round. Index + 1 [1-4]
        game_rounds.append(
            GameRound(
                next_word.word,
                translations,
                next_word.translation,
                correct_index + 1
            ))

    return game_rounds


def mix_list(my_list):
    list_length = len(my_list)
    tmp_list = my_list.copy()
    new_list = []
    for i in range(list_length):
        new_list.append(
            tmp_list.pop(
                random.randint(0, len(tmp_list) - 1)))

    return new_list


class GameRound:
    """
    Contains word and 4 different translations to guess
    Correct answer and correct answer`s index [1-4] for fast check
    """

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
        return_str += "1. " + self.translation1 + "\n"
        return_str += "2. " + self.translation2 + "\n"
        return_str += "3. " + self.translation3 + "\n"
        return_str += "4. " + self.translation4
        return return_str

    def print_game_round_with_answer(self):
        return_str = self.print_game_round()
        return_str += "Correct {} - {} ".format(self.correct_answer, self.correct_index)
        return return_str


class Model:
    pass
