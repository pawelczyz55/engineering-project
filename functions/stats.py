import pandas as pd
import numpy as np
from scipy import stats

def describeStatistics(df: pd.DataFrame) -> pd.DataFrame:
    stats = df.describe()
    stats = stats.rename(index={0: "Liczba wierszy", 1: "Średnia", 2: "Odchylenie standardowe", 3: "Wartość minimalna", 7: "Wartość maksymalna"})
    return stats

def standarizer(df: pd.Series) -> pd.Series:
    result = stats.zscore(df)
    return result

def iqr(df: pd.Series) -> list:
    Q1 = np.percentile(df, 25, interpolation = 'midpoint')
    Q3 = np.percentile(df, 75, interpolation = 'midpoint')
    IQR = Q3 - Q1

    return [Q1-1.5*IQR, Q3+1.5*IQR]

def remove_outliers(df: pd.DataFrame, column: str, method: str, value: float):
    """
    Remove outliers from data frame.

    Avaiable methods:
        - Z-score
        - IQR (Inter Quartile Range)
        - Percentile
    """
    result_df = df.copy()
    to_drop_down = []
    if method=='Z-score':
        z = np.abs(stats.zscore(result_df[column]))
        to_drop_down = np.where(z > value)[0].tolist()
    elif method=='IQR ':
        IQR_range = iqr(df[column])
        upper = (result_df[column] >= IQR_range[1])
        lower = (result_df[column] <= IQR_range[0])
        to_drop_down = np.where(lower | upper)[0].tolist()
    elif method=='Percentile':
        if value>50:
            p = np.percentile(df[column], [100-value, value])
        else:
            p = np.percentile(df[column], [value, 100-value])
        to_drop_down = result_df[(result_df[column] < p[0]) | (result_df[column] > p[1])].index
    
    droped_nb = len(to_drop_down)
    if droped_nb>0:
        result_df.drop(index=to_drop_down, inplace=True)
            
    return result_df, droped_nb