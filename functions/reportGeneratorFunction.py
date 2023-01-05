import json
import pandas as pd
import plotly
import plotly.express as px

def renameColumnsName(df, newNames):
    newNames = newNames.split(',')
    if len(df.columns) == len(newNames):
        df.columns = newNames
    return df

def barPlot(df, x, y):
    fig = px.bar(df, x , y)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def scatterPlot(df, x, y):
    fig = px.scatter(df, x, y)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def getColumnsNamesInTable(df):
    return ' '.join(str(e) for e in df.columns)