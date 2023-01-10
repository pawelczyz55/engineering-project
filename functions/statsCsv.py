import pandas as pd

def file_statistics(df):
    stats = df.describe()
    stats = stats.rename(index={0: "Liczba wierszy", 1: "Średnia", 2: "Odchylenie standardowe", 3: "Wartość minimalna", 7: "Wartość maksymalna"})
    return stats