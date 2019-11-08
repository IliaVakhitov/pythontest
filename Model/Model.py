import random
import logging
from abc import ABC, abstractmethod
from typing import Optional, List
from Model.Dictionary import Dictionary
from Model.GameRound import GameRound
from Model.GameType import GameType
from View import view


class Model(ABC):
    """ Abstract Class different types of Models
    Contains abstract methods
    Methods
        reset_progress - to set learning_index = 0
        print_dictionaries - uses view to print
        play_game - to play game with defined list of GameRound
    """

    @abstractmethod
    def save_state(self):
        pass

    @abstractmethod
    def load_dictionaries(self):
        pass

    @abstractmethod
    def generate_game(self,
                      game_type: GameType,
                      words_number: int = 0,
                      dictionaries: Optional[List[str]] = None) -> Optional[List[GameRound]]:
        pass

    def reset_progress(self, words):
        for word_entry in words:
            word_entry.set_learn_index(0)

    def print_dictionaries(self, dictionaries: List[Dictionary]) -> None:
        for dictionary in dictionaries:
            view.print_str(dictionary.print_information())

    @staticmethod
    def play_game(game_rounds: Optional[List[GameRound]], automatic_mode: bool = False) -> None:
        if game_rounds is None:
            logging.info("No game rounds! Game is over!")
            print("Game over!")
            return None
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
                index = random.randint(1, 4)
            else:
                index = view.input_user_answer("Please, choose a word:")

            logging.info("User answer {} is {}".format(
                index,
                "correct" if game_round.is_index_correct(index) else "incorrect"))
            if game_round.is_index_correct(index):
                correct_answers += 1
                game_round.dictionary_entry.increase_learn_index()
            else:
                incorrect_answers += 1
                game_round.dictionary_entry.decrease_learn_index()

        logging.info("Game ended. Correct answers {}. Incorrect answers {}".format(correct_answers, incorrect_answers))