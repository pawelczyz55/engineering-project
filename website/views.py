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

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()

            flash("Note added.", category='success')

    return render_template("home.html", user=current_user)

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

    try:
        data = procces_csv('G:\Projekt Inzynierski\csv_data\pnewFile.csv')
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
        newColumsNames = request.form.get('columnNames')
        chartType = form1.chartType.data
        #chartType = "scatter"
        x = request.form.get('x')
        y = request.form.get('y')
        color = request.form.get('color')

        #html = generateReport(csvData,newColumsNames, chartType,x,y)
        if newColumsNames != '':
            csvData = reportGeneratorFunction.renameColumnsName(csvData, newColumsNames)
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
        else:
            graphJSON = reportGeneratorFunction.scatterPlot(csvData)
            html = render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)

        # options = {
        # "orientation": "landscape",
        # "page-size": "A4",
        # "margin-top": "1.0cm",
        # "margin-right": "1.0cm",
        # "margin-bottom": "1.0cm",
        # "margin-left": "1.0cm",
        # "encoding": "UTF-8",
        # }
        # pdf = pdfkit.from_string(html, options)
        
        return html

    return render_template("visualization_and_reporting.html",user=current_user, 
        files=os.listdir('G:\Projekt Inzynierski\csv_data'), 
        tables=[tableOf5.to_html()], 
        dataFound = dataFound, 
        columnsNames = columnsNames,
        form1 = form1
        )