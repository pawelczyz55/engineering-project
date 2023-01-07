import pandas as pd

def procces_csv(filepath):
    """
    Function read csv file and save it to pandas Data Frame.

    Input:
        - filepath (string) - path of the file to read

    Return:
        - output_data (DataFrame) - output Data Frame
    """
    output_data = pd.read_csv(filepath, sep=';', header=None)
    return output_data