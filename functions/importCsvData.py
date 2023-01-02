import pandas as pd

def procces_csv(filepath):
    output_data = pd.read_csv(filepath, sep=';', header=None)
    return output_data