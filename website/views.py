from flask import Blueprint, flash, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import os
import pandas as pd

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
from functions import reportGeneratorFunction

@views.route('/visualization-and-reporting', methods=['POST', 'GET'])
@login_required
def visualization_and_reporting():
    dataFound = False

    try:
        data = procces_csv(r'C:\Users\mjurc\OneDrive\Pulpit\engineering-project\csv_data\pnewFile.csv')
        dataFound = True
    except FileNotFoundError:
        return render_template("visualization_and_reporting.html",user=current_user, dataFound = dataFound)

    tableOf5 = data.head()

    if request.method == 'POST':
        oldColumnName = request.form.get('oldName')
        newColumnName = request.form.get('newName')
        chartType = request.form.get('chart-type')
        #chartType = "scatter"
        x = request.form.get('x')
        y = request.form.get('y')

        data = reportGeneratorFunction.rename_columns(data, {oldColumnName:newColumnName})
        if str(chartType) == "scatter":
            graphJSON = reportGeneratorFunction.scatterPlot(data,x,y)
            return render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)

        elif str(chartType) == "bar":
            graphJSON = reportGeneratorFunction.barPlot(data,x,y)
            return render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)
        else:
            graphJSON = reportGeneratorFunction.scatterPlot(data)
            return render_template("report.html",
                user=current_user, 
                graphJSON = graphJSON)


    #Testowy wykres
    df = pd.DataFrame({
      'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
      'Bananas'],
      'Amount': [4, 1, 2, 2, 4, 5],
      'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
    })


    fig = px.bar(df, x='Fruit', y='Amount', color='City', 
        barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # fig2 = px.scatter(data)
    # graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("visualization_and_reporting.html",user=current_user, 
        files=os.listdir(r'C:\Users\mjurc\OneDrive\Pulpit\engineering-project\csv_data'),
        tables=[tableOf5.to_html()], 
        dataFound = dataFound, 
        graphJSON = graphJSON,
        avaiable_columns=['one','two','three']
        )
