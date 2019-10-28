import codecs
import json


"""
Dictionary entry
    word - word in foreign language , 
    translation  - in native language
    learn index - int in range [0,100]
"""


class DictEntry:

    def __init__(self, word, translation):
        self.word = word
        self.translation = translation
        self.learnIndex = 0

    def set_learn_index(self, value):
        if value < 0:
            self.learnIndex = 0
        elif value >= 100:
            self.learnIndex = 100
        else:
            self.learnIndex = value

    def increase_learn_index(self):
        self.learnIndex += (1 if self.learnIndex < 100 else 0)

    def decrease_learn_index(self):
        self.learnIndex -= (1 if self.learnIndex > 0 else 0)

    def set_word(self, value):
        self.word = value

    def set_translation(self, value):
        self.translation = value

    def print_entry(self):
        return "{} - {} : {}".format(self.word, self.translation, self.learnIndex)


"""
Class stores DictEntries as a list
"""


class Dictionary:

    def __init__(self, dict_name):
        self.name = dict_name
        self.words = []
        self.native_language = ""
        self.foreign_language = ""

    def add_new_entry(self, word, translation):
        self.words.append(DictEntry(word, translation))

    def print_information(self):
        res = self.name + "\n"
        res += "Languages: {} - {} \n".format(self.native_language, self.foreign_language)
        res += self.print_words()
        return res

    def print_words(self):
        res = ""
        for word in self.words:
            res = res + word.print_entry()
            res = res + "\n"

        return res

    def add_dict_entry(self, dict_entry):
        self.words.append(dict_entry)

    def remove_dict_entry(self, dict_entry):
        self.words.remove(dict_entry)


class DictionaryLoader:

    def write_dictionary(self, dictionary):
        pass

    def load_dictionary(self, dictionary):
        pass


class DictionaryLoaderJson(DictionaryLoader):

    def __init__(self):
        self.filename = ""

    def write_dictionary(self, dictionary):
        json_data = self.generate_json_data(dictionary)
        try:
            with codecs.open(self.filename, 'w', "utf-8") as outfile:
                json.dump(json_data, outfile, indent=4, ensure_ascii=False)
        except IOError:
            return False
        return True

    def load_dictionary(self, dictionary):
        try:
            with codecs.open(self.filename, 'r', "utf-8") as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError:
            print("File not found {}".format(self.filename))
            return False
        except IOError:
            print("File read error {}".format(self.filename))
            return False

        dictionary.name = json_data['name']
        dictionary.native_language = json_data['native_language']
        dictionary.foreign_language = json_data['foreign_language']
        dictionary.words.clear()
        for entry in json_data['words']:
            dictionary.words.append(DictEntry(entry['word'], entry['translation']))
        return True

    @staticmethod
    def generate_json_data(dictionary):
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
