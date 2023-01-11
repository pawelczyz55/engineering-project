from flask import Blueprint, flash, render_template, request, flash, jsonify, url_for, redirect, make_response
from flask_login import login_required, current_user
from functions import reportGeneratorFunction, forms, statsCsv
from .models import Note
from . import db
import json
import os
import pandas as pd
import pdfkit
import plotly
import plotly.express as px
from sqlalchemy import exc

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

    #Testowe dane
    df = pd.DataFrame({
      'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
      'Bananas'],
      'Amount': [4, 1, 2, 2, 4, 5],
      'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
    })

    tableOf5 = data.head()
    columnsNames = reportGeneratorFunction.getColumnsNamesInTable(data)
    form1 = forms.Forms()
    #form1.chartType.choices = 

    if request.method == 'POST':
        csvData = data
        # oldColumnName = request.form.get('oldName')
        # newColumnName = request.form.get('newName')
        chartsType = request.form.getlist('optionChartSelected[]')

        #multiple charts parameters in array
        xNames = request.form.getlist('x[]')
        yNames = request.form.getlist('y[]')
        colors = request.form.getlist('color[]')

        #html = generateReport(csvData,newColumsNames, chartType,x,y)
        # if newColumnName != '': # to jeszcze nie dziala
        #     csvData = reportGeneratorFunction.rename_columns(csvData, {oldColumnName:newColumnName})
        
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
        #files=os.listdir(r'csv_data'),
        files=os.listdir(r'C:\Users\mjurc\OneDrive\Pulpit\engineering-project\csv_data'),
        tables=[tableOf5.to_html()], 
        dataFound = dataFound, 
        graphJSON = graphJSON,
        avaiable_columns= data.columns,
        form1 = form1
        )

@views.route('/rename-columns', methods=['GET', 'POST'])
@login_required
def rename_columns():
    dataFound = False
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