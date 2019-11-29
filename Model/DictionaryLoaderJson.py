import codecs
import json
import logging
from typing import List, Optional

from Model.DictEntry import DictEntry
from Model.Dictionary import Dictionary
from Model.DictionaryLoader import DictionaryLoader
from Model.JsonManager import JsonManager


class DictionaryLoaderJson(DictionaryLoader):

    """
    Class allows load and save dictionary form/to JSON-file
    Dictionaries are saved as a list
    Each dictionary contains it`s fields and a list of the words
        filename should be given to operate
    """

    def __init__(self):
        self.filename = ""
        self.json_loader = JsonManager(self.filename)

    def save_dictionaries(self, dictionaries: List[Dictionary]) -> bool:

        return self.json_loader.save_json_data(self.generate_json_data(dictionaries))

    def load_dictionaries(self) -> Optional[List[Dictionary]]:

        """
        Creates list of Dictionaries with values loaded from Json
        :return:
            None if not successful
            List[Dictionary]
        """

        json_data = self.json_loader.load_json_data()

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
