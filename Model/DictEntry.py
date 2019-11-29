
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
