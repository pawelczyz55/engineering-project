import json
import plotly
import plotly.express as px


def barPlot(df, x, y, color):
    if(color != ''):
        fig = px.bar(df, str(x) , str(y), color=color)
    else:
        fig = px.bar(df, str(x) , str(y))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def scatterPlot(df, x, y, color):
    if(color != ''):
        fig = px.scatter(df, x, y, color = color)
    else:
        fig = px.scatter(df, x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def pieChartPlot(df, x, y, color):
    if(color != ''):
        fig = px.pie(df, x, y, color = color)
    else:
        fig = px.pie(df, x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def linePlot(df, x, y, color):
    if(color != ''):
        fig = px.line(df, x, y, color = color)
    else:
        fig = px.line(df, x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def lineAreaPlot(df, x, y, color):
    if(color != ''):
        fig = px.area(df, x, y, color = color)
    else:
        fig = px.area(df, x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def histogramPlot(df, x, y, color):
    if(color != ''):
        fig = px.histogram(df, x, y, color = color)
    else:
        fig = px.histogram(df, x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def boxPlot(df, x, y, color):
    if(color != ''):
        fig = px.box(df, x, y, color = color)
    else:
        fig = px.box(df, x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def singleBoxPlot(df, x, title, col):
    fig = px.box(df, x, color_discrete_sequence=col)
    fig.update_layout(
        title={
            'text': title,
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def violinPlot(df, x, y, color):
    if(color != ''):
        fig = px.violin(df, x, y, color = color)
    else:
        fig = px.violin(df, x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def heatmapPlot(df, x, y, color):
    if(color != ''):
        fig = px.density_heatmap(df, x, y)
    else:
        fig = px.density_heatmap(df, x, y)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON