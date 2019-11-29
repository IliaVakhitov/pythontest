import codecs
import json
import logging
from json import JSONDecodeError


class JsonManager:

    def __init__(self, filename: str):
        self.filename: str = filename

    def save_json_data(self, json_data) -> bool:

        try:
            with codecs.open(self.filename, 'w', "utf-8") as outfile:
                json.dump(json_data, outfile, indent=4, ensure_ascii=False)
        except IOError:
            logging.error(f"Error writing file \'{self.filename}\'")
            return False

        return True

    def load_json_data(self):
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

        return json_data
