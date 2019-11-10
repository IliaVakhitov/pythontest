import logging
import random
from typing import List, Optional
from Model.Dictionary import DictEntry
from Model.GameRound import GameRound
from Model.GameType import GameType


class GameGenerator:

    """
    Class is used to generate list of GameRounds
    """

    @staticmethod
    def mix_list(item_list) -> List:

        """
        Function allows to mix elements in list
        :param item_list: initial list
        :return: List - new mixed list
        """

        list_length = len(item_list)
        tmp_list = item_list.copy()
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

        """
        Function allows to get random translation or spelling from given list of DictEntries
        :param all_words: Source list of DictEntries
        :param game_type: Defines what to return spelling or translation
        :param used_value: correct answer. This value is ignored
        :param used_values: this values will be ignored
        :return: str spelling or translation
        """

        new_word = all_words[random.randint(0, len(all_words) - 1)]
        if game_type == GameType.FindTranslation:
            while new_word.translation == used_value or new_word.translation in used_values:
                new_word = all_words[random.randint(0, len(all_words) - 1)]
        elif game_type == GameType.FindSpelling:
            while new_word.spelling == used_value or new_word.spelling in used_values:
                new_word = all_words[random.randint(0, len(all_words) - 1)]

        return_value = ""
        if game_type == GameType.FindTranslation:
            return_value = new_word.translation
        elif game_type == GameType.FindSpelling:
            return_value = new_word.spelling
        return return_value

    @staticmethod
    def generate_game(
            words_list: List[DictEntry],
            game_type: GameType,
            words_number: int = 0) -> Optional[List[GameRound]]:

        """
        Generates list of GameRounds
        Does not make sense if words_number < 4. Return None in this case
        :param words_list: list to generate game roynds
        :param game_type: enum
        :param words_number: 0 or higher than 3
        :return:
            None - if no words is dictionaries or words less than 4
            List of GameRounds:
        """

        if len(words_list) == 0:
            # No words in dictionaries
            logging.info("No words in dictionaries!")
            return None

        if len(words_list) < 4:
            logging.info("Not enough words to generate game!")
            return None

        game_rounds: List[GameRound] = []

        all_words = GameGenerator.mix_list(words_list)
        for next_word in all_words:
            # For each entry generating 3 random translations/spellings
            # Correct answer inserted before getting random translations

            if 0 < words_number <= len(game_rounds):
                break

            # index for correct answer
            correct_index = random.randint(0, 3)

            value = ""
            if game_type == GameType.FindTranslation:
                value = next_word.translation
            elif game_type == GameType.FindSpelling:
                value = next_word.spelling
            translations = []
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
                        next_word.spelling,
                        translations,
                        next_word.translation,
                        correct_index + 1
                    ))
            elif game_type == GameType.FindSpelling:
                game_rounds.append(
                    GameRound(
                        next_word,
                        next_word.translation,
                        translations,
                        next_word.spelling,
                        correct_index + 1
                    ))

        return game_rounds
