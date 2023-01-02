import pandas as pd
import os

class InputCsv:
    data = None


    def __init__(self, base_path, file_name):
        self.base_path = base_path
        self.file_name = file_name

    def read_data(self, sep=';'):
        full_filepath = os.path.join(self.base_path, self.file_name)
        self.data = pd.read_csv(full_filepath, sep=sep)