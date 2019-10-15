
class Model:
    pass


class DictEntry():
    word = ""
    translation = ""
    learnIndex = 0

    def __init__(self, word, translation):
        self.word = word
        self.translation = translation

    def setLearnIndex(self, value):
        self.learnIndex = value

    def setWord(self, value):
        self.word = value

    def setTranslation(self, value):
        self.translation = value

    def printEntry(self):
        return "{} - {} : {}".format(self.word, self.translation, self.learnIndex)


class Dictionary:
    words = []

    def addNewEntry(self, word, translation):
        self.words.append(DictEntry(word, translation))

    def printWords(self):
        res = ""
        for word in self.words:
            res = res + word.printEntry()
            res = res + "\n"

        return res