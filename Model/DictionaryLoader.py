from abc import ABC, abstractmethod
from typing import List

from Model.Dictionary import Dictionary


class DictionaryLoader(ABC):

    """
    Abstract class to load/save dictionaries
    """
    @abstractmethod
    def save_dictionaries(self, dictionaries: List[Dictionary]):
        pass

    @abstractmethod
    def load_dictionaries(self):
        pass