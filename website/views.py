from flask import Blueprint, flash, render_template, request, flash, jsonify, url_for, redirect, make_response
from flask_login import login_required, current_user
from functions import reportGeneratorFunction, statsCsv
from .models import Note
from . import db
import json
import os
import pandas as pd
import pdfkit
from sqlalchemy import exc

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
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
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/reports', methods=['POST', 'GET'])
@login_required
def reports():
    return render_template("reports.html", user=current_user)

@views.route('/visualization-and-reporting', methods=['POST', 'GET'])
@login_required
def visualization_and_reporting():
    dataFound = False
    try:
        db_connector = db.get_engine().connect()
        data = pd.read_sql('test', db_connector)
        dataFound = True
        db_connector.close()
    except (exc.SQLAlchemyError, exc.DatabaseError):
        return render_template("visualization_and_reporting.html",user=current_user, dataFound = dataFound)

    tableOf5 = data.head()
    optionsChart = ["barplot", "scatterplot", "piechartplot", "lineplot", "lineareaplot",
                    "histogramplot", "boxplot", "violinplot", "heatmapplot"]

    if request.method == 'POST':
        csvData = data
        chartsType = request.form.getlist('optionChartSelected[]')

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
        chartsQuantity = len(graphJSONtable)
        html = render_template("report.html", user=current_user, graphJSONtable = graphJSONtable,
                                    graphJSON = graphJSONtable[0], chartsQuantity = chartsQuantity)
        return html

    return render_template("visualization_and_reporting.html",user=current_user, 
        tables=[tableOf5.to_html()], 
        dataFound = dataFound,
        optionsToSelect = optionsChart
        )

@views.route('/rename-columns', methods=['GET', 'POST'])
@login_required
def rename_columns():
    dataFound = False
    # Get table from data base
    try:
        db_connector = db.get_engine().connect()
        data = pd.read_sql('test', db_connector)
        dataFound = True
        cols = data.columns.tolist()
    except (exc.SQLAlchemyError, exc.DatabaseError):
        return render_template("visualization_and_reporting.html",user=current_user, dataFound = dataFound)

    if request.method == 'POST':

        col_to_rename = {}
        for i in range(len(cols)):
            new_name = request.form.get(f'new_column_name_{i}')
            if new_name!='':
                col_to_rename[cols[i]] = new_name
        
        data = data.rename(columns=col_to_rename)        
        try:
            data.to_sql('test', db_connector, if_exists='replace', index=False)
            db_connector.close()
        except (exc.ArgumentError, exc.DatabaseError):
            return render_template('rename_columns.html', columns=cols, len=len(cols), repet=False)

        return redirect(url_for('views.visualization_and_reporting'))

    return render_template('rename_columns.html', columns=cols, len=len(cols), repet=True)