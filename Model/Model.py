from Model.GameGenerator import GameGenerator
from Model.GameRound import GameRound
from Model.GameType import GameType
from View import view
from Model.Dictionary import Dictionary, DictionaryLoadedXls, DictEntry, DictionaryLoaderJson
import os
import random
import logging
from typing import List, Optional


class Model:
    """ Class uses to play console game.
    Two types of games are available
    Words number can be defined
    Always all dictionaries are used
    """
    def __init__(self):
        self.dictionaries: List[Dictionary] = []
        self.all_words: List[DictEntry] = []
        self.dictionary_handler: DictionariesHandler = DictionariesHandler(self)

    def save_dictionaries(self):
        self.dictionary_handler.save_dictionaries()

    def load_dictionaries(self):
        self.dictionary_handler.load_dictionaries()

    def generate_game(self, game_type: GameType, words_number=0) -> Optional[List[GameRound]]:
        return GameGenerator.generate_game(self.all_words, game_type, words_number)

    def reset_progress(self):
        for word_entry in self.all_words:
            word_entry.set_learn_index(0)

    @staticmethod
    def play_game(game_rounds, automatic_mode: bool = False) -> None:
        view.print_str("Game starts!")
        view.print_str("Print exit() for exit")
        logging.info("New game started")
        correct_answers = 0
        incorrect_answers = 0
        for game_round in game_rounds:
            view.print_str(game_round.print_game_round())
            logging.info("Word {} correct answer {}".format(game_round.word, game_round.correct_index))
            # Get user input or generate user input
            if automatic_mode:
                index = random.randint(1,4)
            else:
                index = view.input_user_answer("Please, choose correct word:")

            logging.info("User answer {} is {}".format(
                index,
                "correct" if game_round.is_index_correct(index) else "incorrect"))
            if game_round.is_index_correct(index):
                correct_answers += 1
                game_round.dictionary_entry.increase_learn_index()
                # view.print_str("Correct!")
            else:
                incorrect_answers += 1
                game_round.dictionary_entry.decrease_learn_index()
                # view.print_str("InCorrect!")
        logging.info("Game ended. Correct answers {}. Incorrect answers {}". format(correct_answers, incorrect_answers))


class DictionariesHandler:
    """ Used to load and save dictionaries from dir \\Dictionaries\\
        Called from model
        Saving always in JSON
        Loading from JSON and XLS
    """

    def __init__(self, model: Model) -> None:
        self.model = model

    def save_dictionaries(self) -> None:
        logging.info("Saving dictionaries.")
        dictionary_loader_json = DictionaryLoaderJson()
        dictionary_loader_json.filename = "Dictionaries\\dictionaries.json"
        dictionary_loader_json.save_dictionaries(self.model.dictionaries)

    def load_dictionaries(self) -> None:
        logging.info("Loading dictionaries.")
        dictionary_loader_json = DictionaryLoaderJson()
        dictionary_loader_xls = DictionaryLoadedXls()
        for file in os.listdir("Dictionaries"):
            # Loading JSON files
            if file.endswith(".json"):
                logging.info("Start reading file {}".format(os.path.join("Dictionaries", file)))
                dictionary_loader_json.filename = os.path.join("Dictionaries", file)
                json_dictionaries = dictionary_loader_json.load_dictionaries()
                self.model.dictionaries += json_dictionaries
                for dictionary in json_dictionaries:
                    self.model.all_words += dictionary.words

            if file.endswith(".xls"):
                # Loading XLS files
                logging.info("Start reading file {}".format(os.path.join("Dictionaries", file)))
                dictionary_loader_xls.filename = os.path.join("Dictionaries", file)
                xls_dictionaries = dictionary_loader_xls.load_dictionaries()
                if xls_dictionaries is not None:
                    self.model.dictionaries += xls_dictionaries
                    for dictionary in xls_dictionaries:
                        self.model.all_words += dictionary.words

        logging.info("Total dictionaries loaded {}".format(len(self.model.dictionaries)))

    def print_dictionaries(self) -> None:
        for dictionary in self.model.dictionaries:
            view.print_str(dictionary.print_information())

