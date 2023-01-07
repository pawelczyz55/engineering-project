import pandas as pd
import os

class InputCsv:
    """
    Class read specified '.csv' file and stores data in Data Frame.
    """
    
    data = None


    def __init__(self, base_path, file_name):
        self.base_path = base_path
        self.file_name = file_name

    def read_data(self, sep=';'):
        full_filepath = os.path.join(self.base_path, self.file_name)
        self.data = pd.read_csv(full_filepath, sep=sep)


def procces_csv(filepath: str):
    """
    Read csv file and save it to pandas Data Frame.

    Input:
        - filepath (string) - path of the file to read

    Return:
        - output_data (DataFrame) - output Data Frame
    """
    output_data = pd.read_csv(filepath, sep=';', header=None)
    return output_data

def transform_df(df: pd.DataFrame):
    """
    Transporma a dataframe. From matrix  m x n, return matrix  n x m.
    """
    return df.T

def renameColumnsName(df: pd.DataFrame, newNames: list):
    newNames = newNames.split(',')
    if len(df.columns) == len(newNames):
        df.columns = newNames
    return df

def rename_columns(df: pd.DataFrame, new_names: dict):
    """
    Rename selected columns into given new names. Column to change should be given in dictionary.
    Example of use:
    >>>  col_to_rename = {old_column_name1: new_name1, old_column_name2: new_name2}
    >>>  rename_columns(df, col_to_rename)
    """
    return df.rename(columns=new_names)