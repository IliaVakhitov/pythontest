import os
import logging
from Model.GameGenerator import GameGenerator
from Model.GameRound import GameRound
from Model.GameType import GameType
from Model.Model import Model
from Model.Dictionary import Dictionary
from Model.DictEntry import DictEntry
from Model.DictionaryLoadedXls import DictionaryLoadedXls
from Model.DictionaryLoaderJson import DictionaryLoaderJson
from typing import List, Optional


class ModelConsole(Model):

    """ Class uses to play console game.
    Two types of games are available
    Words number can be defined
    Always all dictionaries are used
    """

    def __init__(self) -> None:

        self.dictionaries: List[Dictionary] = []
        self.words: List[DictEntry] = []

    def save_state(self, game_rounds: List[GameRound]) -> None:

        """
        Saves dictionaries in JSON file
        :return: None
        """

        logging.info("Saving dictionaries.")
        dictionary_loader_json = DictionaryLoaderJson()
        dictionary_loader_json.filename = "Dictionaries\\dictionaries.json"
        dictionary_loader_json.save_dictionaries(self.dictionaries)

    def load_dictionaries(self):

        logging.info("Loading dictionaries.")
        dictionary_loader_json = DictionaryLoaderJson()
        dictionary_loader_xls = DictionaryLoadedXls()
        for file in os.listdir("Dictionaries"):
            # Loading JSON files
            if file.endswith(".json"):
                logging.info("Start reading file {}".format(os.path.join("Dictionaries", file)))
                dictionary_loader_json.filename = os.path.join("Dictionaries", file)
                json_dictionaries = dictionary_loader_json.load_dictionaries()
                self.dictionaries += json_dictionaries
                for dictionary in json_dictionaries:
                    self.words += dictionary.words

            if file.endswith(".xls"):
                # Loading XLS files
                logging.info("Start reading file {}".format(os.path.join("Dictionaries", file)))
                dictionary_loader_xls.filename = os.path.join("Dictionaries", file)
                xls_dictionaries = dictionary_loader_xls.load_dictionaries()
                if xls_dictionaries is not None:
                    self.dictionaries += xls_dictionaries
                    for dictionary in xls_dictionaries:
                        self.words += dictionary.words

        logging.info("Total dictionaries loaded {}".format(len(self.dictionaries)))

    def generate_game(self,
                      game_type: GameType,
                      words_number: int = 0,
                      dictionaries: Optional[List[str]] = None) -> Optional[List[GameRound]]:

        return GameGenerator.generate_game(self.words, game_type, words_number)

    def reset_progress(self, words):

        super().reset_progress(words)

    def print_dictionaries(self,  dictionaries: List[Dictionary]) -> None:

        super().print_dictionaries(dictionaries)

    def play_game(self, game_rounds: List[GameRound], automatic_mode: bool = False) -> None:

        super().play_game(game_rounds, automatic_mode)


