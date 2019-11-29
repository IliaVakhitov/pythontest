import codecs
import json
import logging
from json import JSONDecodeError
from typing import List

from Model.Dictionary import Dictionary
from Model.DictEntry import DictEntry
from Model.DictionaryLoader import DictionaryLoader


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
        except IOError:
            logging.error(f"Error writing file \'{self.filename}\'")
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
                dictionary.words.append(
                    DictEntry(
                        word_entry['word'],
                        word_entry['translation'],
                        word_entry['learnIndex']))

            logging.info(f"Dictionary \'{dictionary.name}\' added. Total words \'{len(dictionary.words)}\'")
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
