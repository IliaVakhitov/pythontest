from Model.model import *
from Model.Dictionary import DictionaryLoaderJson
from Test.ModelTestClasses import ModelTests

load_dictionaries()
print_dictionaries()
dict_loader = DictionaryLoaderJson()
for dictionary in my_dictionaries:
    dict_loader.filename = "Dictionaries\\" + dictionary.name + ".json"
    dict_loader.write_dictionary(dictionary)

