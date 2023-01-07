from flask import Blueprint, flash, render_template, request, flash, jsonify, url_for, redirect, make_response
from flask_login import login_required, current_user
from functions import statsCsv
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

@views.route('/test', methods=['POST', 'GET'])
@login_required
def testowy():
    df = px.data.iris()
    stats = statsCsv.file_statistics(df)
 
    return render_template("testowy.html", stats=[stats.to_html()] )

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
    form1 = forms.Forms()
    #form1.chartType.choices = 

    if request.method == 'POST':
        csvData = df
        oldColumnName = request.form.get('oldName')
        newColumnName = request.form.get('newName')
        chartType = form1.chartType.data
        #chartType = "scatter"
        x = request.form.get('x')
        y = request.form.get('y')
        color = request.form.get('color')

        #html = generateReport(csvData,newColumsNames, chartType,x,y)
        if newColumnName != '': # to jeszcze nie dziala
            csvData = reportGeneratorFunction.rename_columns(csvData, {oldColumnName:newColumnName})
        if str(chartType) == "scatterplot":
            graphJSON = reportGeneratorFunction.scatterPlot(csvData,x,y,color)
            html = render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)

        elif str(chartType) == "barplot":
            graphJSON = reportGeneratorFunction.barPlot(csvData,x,y,color)
            html = render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)

        elif str(chartType) == "piechartplot":
            graphJSON = reportGeneratorFunction.pieChartPlot(csvData,x,y,color)
            html = render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)

        elif str(chartType) == "lineplot":
            graphJSON = reportGeneratorFunction.linePlot(csvData,x,y,color)
            html = render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)

        elif str(chartType) == "lineareaplot":
            graphJSON = reportGeneratorFunction.lineAreaPlot(csvData,x,y,color)
            html = render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)

        elif str(chartType) == "histogramplot":
            graphJSON = reportGeneratorFunction.histogramPlot(csvData,x,y,color)
            html = render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)

        elif str(chartType) == "boxplot":
            graphJSON = reportGeneratorFunction.boxPlot(csvData,x,y,color)
            html = render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)

        elif str(chartType) == "violinplot":
            graphJSON = reportGeneratorFunction.violinPlot(csvData,x,y,color)
            html = render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)

        elif str(chartType) == "heatmapplot":
            graphJSON = reportGeneratorFunction.heatmapPlot(csvData,x,y,color)
            html = render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)

        else:
            graphJSON = reportGeneratorFunction.scatterPlot(csvData)
            html = render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)
        
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
        form1 = form1
        )
