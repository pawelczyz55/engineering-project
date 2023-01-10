from flask import Blueprint, flash, render_template, request, flash, jsonify, url_for, redirect, make_response
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import os
import pandas as pd
import pdfkit

from functions.importCsvData import procces_csv

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    """
    Function render Notes tab page.

    Return:
        - string - template name of 'notes.html'
        - user - data of current loged in user
    """
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()

            flash("Note added.", category='success')

    return render_template("notes.html", user=current_user )

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


import plotly
import plotly.express as px
from functions import reportGeneratorFunction, forms

@views.route('/visualization-and-reporting', methods=['POST', 'GET'])
@login_required
def visualization_and_reporting():
    dataFound = False
    filename = 'pnewFile.csv'
    location = f'csv_data\{filename}'

    try:
        data = procces_csv(location)
        dataFound = True
    except FileNotFoundError:
        return render_template("visualization_and_reporting.html",user=current_user, dataFound = dataFound)

    #Testowe dane
    df = pd.DataFrame({
      'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
      'Bananas'],
      'Amount': [4, 1, 2, 2, 4, 5],
      'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
    })

    tableOf5 = df.head()
    columnsNames = reportGeneratorFunction.getColumnsNamesInTable(df)
    optionsChart = ["barplot", "scatterplot", "piechartplot", "lineplot", "lineareaplot", "histogramplot", "boxplot", "violinplot", "heatmapplot"]
    form1 = forms.Forms()
    tablesTest=[tableOf5.to_html()]
    #form1.chartType.choices = 

    if request.method == 'POST':
        csvData = df
        oldColumnName = request.form.get('oldName')
        newColumnName = request.form.get('newName')
        chartsType = request.form.getlist('optionChartSelected[]')
        print(chartsType)

        #multiple charts parameters in array
        xNames = request.form.getlist('x[]')
        yNames = request.form.getlist('y[]')
        colors = request.form.getlist('color[]')

        graphJSONtable = []
        for i in range(len(chartsType)):
            if str(chartsType[i]) == "scatterplot":
                graphJSON = reportGeneratorFunction.scatterPlot(csvData,xNames[i],yNames[i],colors[i])
                graphJSONtable.append(graphJSON)

            elif str(chartsType[i]) == "barplot":
                graphJSON = reportGeneratorFunction.barPlot(csvData,xNames[i],yNames[i],colors[i])
                graphJSONtable.append(graphJSON)

            elif str(chartsType[i]) == "piechartplot":
                graphJSON = reportGeneratorFunction.pieChartPlot(csvData,xNames[i],yNames[i],colors[i])
                graphJSONtable.append(graphJSON)

            elif str(chartsType[i]) == "lineplot":
                graphJSON = reportGeneratorFunction.linePlot(csvData,xNames[i],yNames[i],colors[i])
                graphJSONtable.append(graphJSON)

            elif str(chartsType[i]) == "lineareaplot":
                graphJSON = reportGeneratorFunction.lineAreaPlot(csvData,xNames[i],yNames[i],colors[i])
                graphJSONtable.append(graphJSON)

            elif str(chartsType[i]) == "histogramplot":
                graphJSON = reportGeneratorFunction.histogramPlot(csvData,xNames[i],yNames[i],colors[i])
                graphJSONtable.append(graphJSON)

            elif str(chartsType[i]) == "boxplot":
                graphJSON = reportGeneratorFunction.boxPlot(csvData,xNames[i],yNames[i],colors[i])
                graphJSONtable.append(graphJSON)

            elif str(chartsType[i]) == "violinplot":
                graphJSON = reportGeneratorFunction.violinPlot(csvData,xNames[i],yNames[i],colors[i])
                graphJSONtable.append(graphJSON)

            elif str(chartsType[i]) == "heatmapplot":
                graphJSON = reportGeneratorFunction.heatmapPlot(csvData,xNames[i],yNames[i],colors[i])
                graphJSONtable.append(graphJSON)

            else:
                graphJSON = reportGeneratorFunction.scatterPlot(csvData)
                graphJSONtable.append(graphJSON)

        #print(graphJSONtable)
        html = render_template("report.html", user=current_user, graphJSONtable = graphJSONtable, graphJSON = graphJSONtable[0])
        return html


    fig = px.bar(df, x='Fruit', y='Amount', color='City', 
        barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # fig2 = px.scatter(data)
    # graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("visualization_and_reporting.html",user=current_user, 
        files=os.listdir(r'csv_data'),
        tables=[tableOf5.to_html()], 
        dataFound = dataFound, 
        graphJSON = graphJSON,
        avaiable_columns= df.columns,
        optionsToSelect = optionsChart,
        form1 = form1
        )
