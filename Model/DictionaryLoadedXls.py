import logging
import xlrd
from typing import List
from Model.Dictionary import Dictionary
from Model.DictionaryLoader import DictionaryLoader


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
