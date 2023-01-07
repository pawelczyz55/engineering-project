import json
import pandas as pd
import plotly
import plotly.express as px

def renameColumnsName(df, newNames: str):
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

def barPlot(df, x, y, color):
    if(color != ''):
        fig = px.bar(df, x , y, color=color)
    else:
        fig = px.bar(df, x , y)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def scatterPlot(df, x, y, color):
    if(color != ''):
        fig = px.scatter(df, x, y, color = color)
    else:
        fig = px.scatter(df, x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def getColumnsNamesInTable(df):
    return ' '.join(str(e) for e in df.columns)