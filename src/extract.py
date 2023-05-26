import os
import logging
from .utils import *


class Extractor():

    def __init__(self, path: str):
        self.path = path

    def extract(self):
        if self.is_directory():
            return self.get_directory_content()
        else:
            return self.read_file()

    def is_directory(self) -> bool:
        return os.path.isdir(self.path)

    def get_directory_content(self) -> str:
        file_contents = []
        for filename in os.listdir(self.path):
            file_path = os.path.join(self.path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    file_contents.append(content)
        return file_contents

    def read_file(self) -> str:
        try:
            with open(self.path, "r") as f:
                return f.read(10000)
        except FileNotFoundError:
            logging.error(f"File not found: {self.path}")
            return None
        except Exception as e:
            logging.error(f"Error reading file: {self.path}, {e}")
            return None
