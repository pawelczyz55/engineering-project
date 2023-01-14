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

@views.route('/reports', methods=['POST', 'GET'])
@login_required
def reports():
    return render_template("reports.html", user=current_user)

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
            summaryTable = [statsCsv.file_statistics(data).to_html()]

            # multiple charts parameters in array
            xNames = request.form.getlist('x[]')
            yNames = request.form.getlist('y[]')
            colors = request.form.getlist('color[]')
            titles = request.form.getlist('titles[]')
            
            graphJSONtable = []
            for i in range(len(chartsType)):
                if str(chartsType[i]) == "scatterplot":
                    graphJSON = reportGeneratorFunction.scatterPlot(csvData,xNames[i],yNames[i],colors[i],titles[i])
                    graphJSONtable.append(graphJSON)

                elif str(chartsType[i]) == "barplot":
                    graphJSON = reportGeneratorFunction.barPlot(csvData,xNames[i],yNames[i],colors[i],titles[i])
                    graphJSONtable.append(graphJSON)

                elif str(chartsType[i]) == "piechartplot":
                    graphJSON = reportGeneratorFunction.pieChartPlot(csvData,xNames[i],yNames[i],colors[i],titles[i])
                    graphJSONtable.append(graphJSON)

                elif str(chartsType[i]) == "lineplot":
                    graphJSON = reportGeneratorFunction.linePlot(csvData,xNames[i],yNames[i],colors[i],titles[i])
                    graphJSONtable.append(graphJSON)

                elif str(chartsType[i]) == "lineareaplot":
                    graphJSON = reportGeneratorFunction.lineAreaPlot(csvData,xNames[i],yNames[i],colors[i],titles[i])
                    graphJSONtable.append(graphJSON)

                elif str(chartsType[i]) == "histogramplot":
                    graphJSON = reportGeneratorFunction.histogramPlot(csvData,xNames[i],yNames[i],colors[i],titles[i])
                    graphJSONtable.append(graphJSON)

                elif str(chartsType[i]) == "boxplot":
                    graphJSON = reportGeneratorFunction.boxPlot(csvData,xNames[i],yNames[i],colors[i],titles[i])
                    graphJSONtable.append(graphJSON)

                elif str(chartsType[i]) == "violinplot":
                    graphJSON = reportGeneratorFunction.violinPlot(csvData,xNames[i],yNames[i],colors[i],titles[i])
                    graphJSONtable.append(graphJSON)

                elif str(chartsType[i]) == "heatmapplot":
                    graphJSON = reportGeneratorFunction.heatmapPlot(csvData,xNames[i],yNames[i],colors[i],titles[i])
                    graphJSONtable.append(graphJSON)

                else:
                    graphJSON = reportGeneratorFunction.scatterPlot(csvData)
                    graphJSONtable.append(graphJSON)

            chartsQuantity = len(graphJSONtable)
            html = render_template("report.html", user=current_user, graphJSONtable = graphJSONtable,
                                        graphJSON = graphJSONtable[0], chartsQuantity = chartsQuantity,
                                        titles=titles, showSummaryTable=showSummaryTable, tables=summaryTable)
            return html

    except TypeError:
        # print info about misspelling in input fields
        flash('Something went wrong. Pleas try select char types and check column spelling', category='error')

    # Render empty page when data not uploaded
    return render_template("visualization_and_reporting.html",user=current_user, 
        tables=[tableOf5.to_html()], 
        dataFound = dataFound,
        optionsToSelect = optionsChart
        )

@views.route('/rename-columns', methods=['GET', 'POST'])
@login_required
def rename_columns():
    dataFound = False
    # Get data from data base
    try:
        db_connector = db.get_engine().connect()
        data = pd.read_sql('uploaded_data', db_connector)
        dataFound = True
        cols = data.columns.tolist()
    except (exc.SQLAlchemyError, exc.DatabaseError):
        return render_template("visualization_and_reporting.html",user=current_user, dataFound = dataFound)

    if request.method == 'POST':
        # Set dictionary of columns to change from input data
        col_to_rename = {}
        for i in range(len(cols)):
            new_name = request.form.get(f'new_column_name_{i}')
            if new_name!='':
                col_to_rename[cols[i]] = new_name
        # process column renaming
        data = data.rename(columns=col_to_rename)        
        try:
            data.to_sql('uploaded_data', db_connector, if_exists='replace', index=False)
            db_connector.close()
        except (exc.ArgumentError, exc.DatabaseError):
            # render error page
            return render_template('rename_columns.html', columns=cols, len=len(cols), repet=False)

        # return to visualisation page apply click on
        return redirect(url_for('views.visualization_and_reporting'))

    # Render page for renaming a columns
    return render_template('rename_columns.html', columns=cols, len=len(cols), repet=True)

@views.route('/standarization', methods=['GET', 'POST'])
@login_required
def standarization():
    dataFound = False
    # Get table from data base
    try:
        db_connector = db.get_engine().connect()
        data = pd.read_sql('uploaded_data', db_connector)
        dataFound = True
        all_cols = data.columns.tolist()
        cols = [col for col in all_cols if pd.api.types.is_numeric_dtype(data[col])]
    except (exc.SQLAlchemyError, exc.DatabaseError):
        return render_template("visualization_and_reporting.html",user=current_user, dataFound = dataFound)

    if request.method == 'POST':
        # Load input data
        col_to_add_as_standarized= []
        col_to_standarize_and_replace = []
        # iterate over input rows equal to columns
        for i in range(len(cols)):
            value = request.form.get(f'standarization_col_{i}')
            if value=='new_column':
                col_to_add_as_standarized.append(cols[i])
            elif value=='replace_column':
                col_to_standarize_and_replace.append(cols[i])

        # process column standarization
        # for 


        db_connector.close()

        return redirect(url_for('views.visualization_and_reporting'))

    db_connector.close()

    return render_template('standarization.html', columns=cols, len=len(cols), repet=True)

@views.route('/remove-outliers', methods=['GET', 'POST'])
@login_required
def outliers():
    return render_template('outliers.html')