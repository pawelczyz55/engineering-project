from flask import Blueprint, flash, render_template, request, flash, jsonify, url_for, redirect, make_response
from flask_login import login_required, current_user
from functions import reportGeneratorFunction, stats
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
        # check correctness of note text
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            # save new note to data base
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            # print information about success save
            flash("Note added.", category='success')

    return render_template("notes.html", user=current_user )

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    # load notes from data base
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            # delete selected note from data base
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/visualization-and-reporting', methods=['POST', 'GET'])
@login_required
def visualization_and_reporting():
    # Load data from data base
    dataFound = False
    try:
        db_connector = db.get_engine().connect()
        data = pd.read_sql('uploaded_data', db_connector)
        dataFound = True
        db_connector.close()
    except (exc.SQLAlchemyError, exc.DatabaseError):
        return render_template("visualization_and_reporting.html",user=current_user, dataFound = dataFound)

    # variable for visualisation
    tableOf5 = data.head()
    optionsChart = ["barplot", "scatterplot", "piechartplot", "lineplot", "lineareaplot",
                    "histogramplot", "boxplot", "violinplot", "heatmapplot"]

    # Cache errors connected with misspelling in input fields
    try:
        if request.method == 'POST':
            # load input data from fields
            csvData = data
            chartsType = request.form.getlist('optionChartSelected[]')
            tmp = request.form.get('ifSummaryCheckbox')
            if request.form.get('ifSummaryCheckbox')=='on':
                showSummaryTable = True
            else:
                showSummaryTable = False
            summaryTable = [stats.describeStatistics(data).to_html()]

            # multiple charts parameters in array
            xNames = request.form.getlist('x[]')
            yNames = request.form.getlist('y[]')
            colors = request.form.getlist('color[]')
            titles = request.form.getlist('titles[]')
            
            graphJSONtable = []
            try:
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

                chartsQuantity = len(graphJSONtable)
                html = render_template("report.html", user=current_user, graphJSONtable = graphJSONtable, chartsQuantity = chartsQuantity,
                                        titles=titles, showSummaryTable=showSummaryTable, tables=summaryTable)

                return redirect(url_for('views.report', html=html))
            except:
                flash("Błędne dane", category='error')

    except TypeError:
        # print info about misspelling in input fields
        flash('Something went wrong. Pleas try select char types and check column spelling', category='error')

    # Render empty page when data not uploaded
    return render_template("visualization_and_reporting.html",user=current_user, 
        tables=[tableOf5.to_html()], 
        dataFound = dataFound,
        optionsToSelect = optionsChart
        )

@views.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    generatedHTML = request.args['html']
    return generatedHTML