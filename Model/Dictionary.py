from typing import List

from Model.DictEntry import DictEntry


class Dictionary:

    """
    Class stores DictEntries as a list
    """

    def __init__(self, dict_name) -> None:

        self.name: str = dict_name
        self.words: List[DictEntry] = []  # DictEntry
        self.native_language: str = ""
        self.foreign_language: str = ""

    def add_new_entry(self, word, translation) -> None:

        self.words.append(DictEntry(word, translation, 0))

    def print_information(self) -> str:

        res = self.name + "\n"
        res += "Languages: {} - {} \n".format(self.native_language, self.foreign_language)
        res += self.print_words()
        return res

    def print_words(self) -> str:

        res = ""
        for word in self.words:
            res = res + word.print_entry()
            res = res + "\n"

        return res

    def add_dict_entry(self, dict_entry) -> None:

        self.words.append(dict_entry)

    def remove_dict_entry(self, dict_entry) -> None:

        self.words.remove(dict_entry)


