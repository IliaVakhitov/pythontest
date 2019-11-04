from View import view
from Model.Dictionary import Dictionary, DictionaryLoadedXls, DictEntry, DictionaryLoaderJson
import os
import random
import logging
from typing import List, Optional
from enum import Enum


class GameType(Enum):
    FindTranslation = 1
    FindWord = 2


class Model:
    def __init__(self):
        self.my_dictionaries: List[Dictionary] = []
        self.all_words: List[DictEntry] = []
        self.dictionary_handler: DictionariesHandler = DictionariesHandler(self)

    def save_dictionaries(self):
        self.dictionary_handler.save_dictionaries()

    def load_dictionaries(self):
        self.dictionary_handler.load_dictionaries()

    def generate_game(self, game_type: GameType, words_number=0):
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


class GameRound:
    """
    Contains word and 4 different translations to guess
    Correct answer and correct answer`s index [1-4] for fast check
    """

    def __init__(self,
                 dictionary_entry: DictEntry,
                 word: str,
                 translations: List[str],
                 correct_answer: str,
                 correct_index: int):

        self.dictionary_entry: DictEntry = dictionary_entry
        self.word: str = word
        self.translation1: str = translations[0]
        self.translation2: str = translations[1]
        self.translation3: str = translations[2]
        self.translation4: str = translations[3]
        self.correct_answer: str = correct_answer
        self.correct_index: int = correct_index

    def is_answer_correct(self, answer) -> bool:
        return answer == self.correct_answer

    def is_index_correct(self, index) -> bool:
        return index == self.correct_index

    def print_game_round(self) -> str:
        return_str = self.word + "\n"
        return_str += "1. " + self.translation1 + "\n"
        return_str += "2. " + self.translation2 + "\n"
        return_str += "3. " + self.translation3 + "\n"
        return_str += "4. " + self.translation4
        return return_str

    def print_game_round_with_answer(self) -> str:
        return_str = self.print_game_round()
        return_str += "Correct {} - {} ".format(self.correct_answer, self.correct_index)
        return return_str


class GameGenerator:
    """ Class is used to generate list of GameRounds
    """
    @staticmethod
    def mix_list(my_list) -> List:
        list_length = len(my_list)
        tmp_list = my_list.copy()
        new_list = []
        for i in range(list_length):
            new_list.append(
                tmp_list.pop(
                    random.randint(0, len(tmp_list) - 1)))

        return new_list

    @staticmethod
    def get_random_translation(
            all_words: List[DictEntry],
            game_type: GameType,
            used_value: str,
            used_values: List[str]) -> str:

        new_word = all_words[random.randint(0, len(all_words) - 1)]
        if game_type == GameType.FindTranslation:
            while (new_word.translation == used_value) or (new_word.translation in used_values):
                new_word = all_words[random.randint(0, len(all_words) - 1)]
        elif game_type == GameType.FindWord:
            while (new_word.word == used_value) or (new_word.word in used_values):
                new_word = all_words[random.randint(0, len(all_words) - 1)]

        return_value = ""
        if game_type == GameType.FindTranslation:
            return_value = new_word.translation
        elif game_type == GameType.FindWord:
            return_value = new_word.word
        return return_value

    @staticmethod
    def generate_game(words_list: List[DictEntry], game_type: GameType, words_number=0) -> Optional[List[GameRound]]:
        """
        Generates list of GameRounds
        return
            None - if no words is dictionaries
            List of GameRounds:
        """
        game_rounds: List[GameRound] = []

        if len(words_list) == 0:
            # No words in dictionaries
            return None

        all_words = GameGenerator.mix_list(words_list)
        for next_word in all_words:
            if 0 < words_number <= len(game_rounds):
                break
            correct_index = random.randint(0, 3)
            translations = []
            value = ""
            if game_type == GameType.FindTranslation:
                value = next_word.translation
            elif game_type == GameType.FindWord:
                value = next_word.word
            for i in range(3):
                translations.append(
                    GameGenerator.get_random_translation(
                        all_words, game_type, value, translations))

            translations.insert(correct_index, value)
            # New game round. Index + 1 [1-4]
            if game_type == GameType.FindTranslation:
                game_rounds.append(
                    GameRound(
                        next_word,
                        next_word.word,
                        translations,
                        next_word.translation,
                        correct_index + 1
                    ))
            elif game_type == GameType.FindWord:
                game_rounds.append(
                    GameRound(
                        next_word,
                        next_word.translation,
                        translations,
                        next_word.word,
                        correct_index + 1
                    ))

        return game_rounds


class DictionariesHandler:
    """ Used to load and save dictionaries from dir \\Dictionaries\\
        Called from model
        Saving always in JSON
        Loading from JSON adn XLS
    """

    def __init__(self, model: Model) -> None:
        self.model = model

    def save_dictionaries(self) -> None:
        logging.info("Saving dictionaries.")
        dictionary_loader_json = DictionaryLoaderJson()
        dictionary_loader_json.filename = "Dictionaries\\dictionaries.json"
        dictionary_loader_json.save_dictionaries(self.model.my_dictionaries)

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
                self.model.my_dictionaries += json_dictionaries
                for my_dict in json_dictionaries:
                    self.model.all_words += my_dict.words

            if file.endswith(".xls"):
                # Loading XLS files
                logging.info("Start reading file {}".format(os.path.join("Dictionaries", file)))
                dictionary_loader_xls.filename = os.path.join("Dictionaries", file)
                xls_dictionaries = dictionary_loader_xls.load_dictionaries()
                if xls_dictionaries is not None:
                    self.model.my_dictionaries += xls_dictionaries
                    for my_dict in xls_dictionaries:
                        self.model.all_words += my_dict.words

        logging.info("Total dictionaries loaded {}".format(len(self.model.my_dictionaries)))

    def print_dictionaries(self) -> None:
        for my_dict in self.model.my_dictionaries:
            view.print_str(my_dict.print_information())

