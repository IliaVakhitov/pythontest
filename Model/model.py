import json

class Model:
    pass


class DictEntry:
    word = ""
    translation = ""
    learnIndex = 0

    def __init__(self, word, translation):
        self.word = word
        self.translation = translation

    def set_learn_index(self, value):
        self.learnIndex = value

    def increase_learn_index(self):
        self.learnIndex += 1

    def decrease_learn_index(self):
        self.learnIndex -= (1 if self.learnIndex >= 1 else 0)

    def set_word(self, value):
        self.word = value

    def set_translation(self, value):
        self.translation = value

    def print_entry(self):
        return "{} - {} : {}".format(self.word, self.translation, self.learnIndex)


class Dictionary:
    words = []
    name = ""
    json_data = {}

    def __init__(self, dict_name):
        self.name = dict_name

    def write_to_json(self, filename):
        self.generate_json_data()
        with open(filename, 'w') as outfile:
            json.dump(self.name, outfile)
            json.dump(self.json_data, outfile)

    def generate_json_data(self):
        json_data = {'name': self.name, 'words': []}
        for word in self.words:
            json_data['words'].append({
                'word': word.word,
                'translation': word.translation,
                'learnIndex': word.learnIndex,
            })

        self.json_data = json_data

    def add_new_entry(self, word, translation):
        self.words.append(DictEntry(word, translation))

    def print_words(self):
        res = ""
        for word in self.words:
            res = res + word.print_entry()
            res = res + "\n"

        return res
