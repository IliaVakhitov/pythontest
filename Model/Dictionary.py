import codecs
import json
import logging
from json import JSONDecodeError
from typing import List

import xlrd as xlrd


class DictEntry:

    """ Dictionary entry
            word - word in foreign language ,
            translation  - in native language
            learn index - int in range [0,100]
    """

    def __init__(self, spelling: str, translation: str, learning_index: int, sql_id: int = 0) -> None:

        self.spelling = spelling
        self.translation = translation
        self.learning_index = learning_index if learning_index > 0 else 0
        self.sql_id = sql_id

    def set_learn_index(self, value) -> None:

        if value < 0:
            self.learning_index = 0
        elif value >= 100:
            self.learning_index = 100
        else:
            self.learning_index = value

    def increase_learn_index(self) -> None:

        self.learning_index += (5 if self.learning_index < 100 else 0)

    def decrease_learn_index(self) -> None:

        self.learning_index -= (5 if self.learning_index > 0 else 0)

    def set_word(self, value) -> None:

        self.spelling = value

    def set_translation(self, value) -> None:

        self.translation = value

    def print_entry(self) -> str:

        return "{} - {} : {}".format(self.spelling, self.translation, self.learning_index)


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


class DictionaryLoader:

    """
    Abstract class to load/save dictionaries
    """

    def save_dictionaries(self, dictionaries: List[Dictionary]):
        pass

    def load_dictionaries(self):
        pass


class DictionaryLoadedXls(DictionaryLoader):

    """
    Class to load/save dictionaries from XLS
    XLS format [Theme, Word, Translation]
    filename should be given to operate
    """

    def __init__(self):
        self.filename = ""

    def save_dictionaries(self, dictionaries: List[Dictionary]):

        super().save_dictionaries(dictionaries)

    def load_dictionaries(self):

        dictionaries: List[Dictionary] = []
        try:
            workbook = xlrd.open_workbook(self.filename)
            worksheet = workbook.sheet_by_index(0)
        except IOError:
            logging.error("Error loading xls file {}".format(self.filename))
            return None

        current_dictionary_name = ""
        current_dictionary = Dictionary("")
        current_dictionary.native_language = "Russian"
        current_dictionary.foreign_language = "English"
        for i in range(1, worksheet.nrows):
            if worksheet.cell(i, 0).value == xlrd.empty_cell.value:
                break
            dictionary_name = worksheet.cell(i, 0).value
            word = worksheet.cell(i, 1).value
            translation = worksheet.cell(i, 2).value
            if current_dictionary_name != dictionary_name and current_dictionary_name != "":
                dictionaries.append(current_dictionary)
                logging.info("Dictionary {} added. Total words {}.".format(
                    current_dictionary.name, len(current_dictionary.words)))

                current_dictionary = Dictionary(dictionary_name)
            if current_dictionary.name != dictionary_name:
                current_dictionary.name = dictionary_name
                current_dictionary.native_language = "Russian"
                current_dictionary.foreign_language = "English"

            current_dictionary.add_new_entry(word, translation)
            current_dictionary_name = dictionary_name
        dictionaries.append(current_dictionary)
        return dictionaries


class DictionaryLoaderJson(DictionaryLoader):

    """
    Class allows load and save dictionary form/to JSON-file
    Dictionaries are saved as a list
    Each dictionary contains it`s fields and a list of the words
        filename should be given to operate
    """

    def __init__(self):
        self.filename = ""

    def save_dictionaries(self, dictionaries: List[Dictionary]) -> bool:
        json_data = self.generate_json_data(dictionaries)
        try:
            with codecs.open(self.filename, 'w', "utf-8") as outfile:
                json.dump(json_data, outfile, indent=4, ensure_ascii=False)
        except:
            logging.error("Error writing file {}".format(self.filename))
            return False

        return True

    def load_dictionaries(self):
        """
        TODO
        :return:
        """
        try:
            with codecs.open(self.filename, 'r', "utf-8") as json_file:
                json_data = json.load(json_file)

        except FileNotFoundError:
            error_message = f"File not found {self.filename}"
            print(error_message)
            logging.error(error_message)
            return None

        except IOError as err:
            error_message = f"File \'{self.filename}\' read error \'{err}\'"
            print(error_message)
            logging.error(error_message)
            return None

        except JSONDecodeError as err:
            error_message = f"Json parse error {err}"
            print(error_message)
            logging.error(error_message)
            return None

        dictionaries: List[Dictionary] = []
        for dict_entry in json_data['dictionaries']:
            dictionary = Dictionary(dict_entry['name'])
            dictionary.native_language = dict_entry['native_language']
            dictionary.foreign_language = dict_entry['foreign_language']
            for word_entry in dict_entry['words']:
                dictionary.words.append(DictEntry(word_entry['word'], word_entry['translation'], word_entry['learnIndex']))

            logging.info("Dictionary {} added. Total words {}.".format(
                dictionary.name, len(dictionary.words)))
            dictionaries.append(dictionary)

        return dictionaries

    @staticmethod
    def generate_json_data(dictionaries: List[Dictionary]):

        json_data = {'dictionaries': []}
        for dictionary in dictionaries:
            dict_json_data = {'name': dictionary.name,
                         'native_language': dictionary.native_language,
                         'foreign_language': dictionary.foreign_language,
                         'words': []}
            for word in dictionary.words:
                dict_json_data['words'].append({
                    'word': word.spelling,
                    'translation': word.translation,
                    'learnIndex': word.learning_index,
                })
            json_data["dictionaries"].append(dict_json_data)
        return json_data
