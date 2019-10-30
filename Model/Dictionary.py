import codecs
import json
import logging
from typing import List

import xlrd as xlrd


class DictEntry:
    """
    Dictionary entry
        word - word in foreign language ,
        translation  - in native language
        learn index - int in range [0,100]
    """

    def __init__(self, word, translation):
        self.word = word
        self.translation = translation
        self.learnIndex = 0

    def set_learn_index(self, value) -> None:
        if value < 0:
            self.learnIndex = 0
        elif value >= 100:
            self.learnIndex = 100
        else:
            self.learnIndex = value

    def increase_learn_index(self) -> None:
        self.learnIndex += (1 if self.learnIndex < 100 else 0)

    def decrease_learn_index(self) -> None:
        self.learnIndex -= (1 if self.learnIndex > 0 else 0)

    def set_word(self, value) -> None:
        self.word = value

    def set_translation(self, value) -> None:
        self.translation = value

    def print_entry(self) -> str:
        return "{} - {} : {}".format(self.word, self.translation, self.learnIndex)


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
        self.words.append(DictEntry(word, translation))

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

    def write_dictionary(self, dictionary):
        pass

    def load_dictionary(self, dictionary):
        pass


class DictionaryLoadedXls(DictionaryLoader):
    def __init__(self):
        self.filename = ""

    def load_dictionaries(self):
        dictionaries: List[Dictionary] = []  # Dictionary
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
    """
    def __init__(self):
        self.filename = ""

    def write_dictionary(self, dictionary: Dictionary) -> bool:
        json_data = self.generate_json_data(dictionary)
        try:
            with codecs.open(self.filename, 'w', "utf-8") as outfile:
                json.dump(json_data, outfile, indent=4, ensure_ascii=False)
        except:
            logging.error("Error writing file {}".format(self.filename))
            return False

        return True

    def load_dictionary(self):
        try:
            with codecs.open(self.filename, 'r', "utf-8") as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError:
            error_message = "File not found {}".format(self.filename)
            print(error_message)
            logging.error(error_message)
            return None
        except IOError:
            error_message = "File read error {}".format(self.filename)
            print(error_message)
            logging.error(error_message)
            return None
        except:
            error_message = "File general error {}".format(self.filename)
            print(error_message)
            logging.error(error_message)
            return None

        dictionary = Dictionary(json_data['name'])
        dictionary.native_language = json_data['native_language']
        dictionary.foreign_language = json_data['foreign_language']
        dictionary.words.clear()
        for entry in json_data['words']:
            dictionary.words.append(DictEntry(entry['word'], entry['translation']))
        logging.info("Dictionary {} added. Total words {}.".format(
            dictionary.name, len(dictionary.words)))

        return dictionary

    @staticmethod
    def generate_json_data(dictionary: Dictionary):
        json_data = {'name': dictionary.name,
                     'native_language': dictionary.native_language,
                     'foreign_language': dictionary.foreign_language,
                     'words': []}
        for word in dictionary.words:
            json_data['words'].append({
                'word': word.word,
                'translation': word.translation,
                'learnIndex': word.learnIndex,
            })

        return json_data
