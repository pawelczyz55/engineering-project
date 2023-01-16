from flask import Blueprint, flash, render_template, request, flash, jsonify, url_for, redirect, make_response
from flask_login import login_required, current_user
from functions import reportGeneratorFunction, stats
from .models import Note
from .views import views
from . import db
import json
import os
import pandas as pd
import pdfkit
from sqlalchemy import exc

transform = Blueprint('transform', __name__)

@transform.route('/rename-columns', methods=['GET', 'POST'])
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
        return render_template("views.visualization_and_reporting.html",user=current_user, dataFound = dataFound)

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
            flash('Input error! Pleas try again.', category='error')
            return render_template('rename_columns.html', columns=cols, len=len(cols), repet=True)

        # return to visualisation page apply click on
        flash(f'Succesfully renamed columns.', category='info')
        return redirect(url_for('views.visualization_and_reporting'))

    # Render page for renaming a columns
    return render_template('rename_columns.html', columns=cols, len=len(cols), repet=True)

@transform.route('/standarization', methods=['GET', 'POST'])
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
        flash('Input error! Pleas try again.', category='error')
        return render_template("standarization.html",user=current_user, dataFound = dataFound)

    if request.method == 'POST':
        # Load input data
        col_to_add_as_standarized= []
        col_to_standarize_and_replace = []
        # iterate over input rows equal to columns
        for i in range(len(cols)):
            value = request.form.get(f'standartCol{i}')
            if value=='newColumn':
                col_to_add_as_standarized.append(cols[i])
            elif value=='replaceColumn':
                col_to_standarize_and_replace.append(cols[i])

        # process column standarization
        for col in col_to_add_as_standarized:
            index = data.columns.get_loc(col)
            data.insert(index+1, f'standarized_{col}', stats.standarizer(data[col]))
        for col in col_to_standarize_and_replace:
            data[col] = stats.standarizer(data[col])
            data = data.rename({col:f'stanadarized_{col}'})

        data.to_sql('uploaded_data', db_connector, if_exists='replace', index=False)
        db_connector.close()

        flash(f'Succesfully standarized columns.', category='info')
        return redirect(url_for('views.visualization_and_reporting'))

    db_connector.close()

    return render_template('standarization.html', columns=cols, len=len(cols), repet=True)

@transform.route('/remove-outliers', methods=['GET', 'POST'])
@login_required
def outliers():
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
        try:
            # Load input data
            method_all_cols = request.form.get('allOutliersMethod')
            methods= []
            values = []
            droped_values_nb = 0
            sth_to_process = False

            if method_all_cols!='selection':
                # read only for all_column selection
                sth_to_process = True
                methods = [method_all_cols]*len(cols)
                val = float(request.form.get('allOutiersValue'))
                if method_all_cols != 'IQR':
                    if val>100 or val<0:
                        raise ValueError
                    values = [val]*len(cols)
            else:
                # read input for every column
                for i in range(len(cols)):
                    method = request.form.get(f'allOutliersMethod_{i}')
                    if method != 'selection' and method != 'IQR':
                        sth_to_process = True
                        val = float(request.form.get(f'allOutiersValue_{i}'))
                        if val>100 or val<0:
                            raise ValueError
                        values.append(val)
                    else:
                        values.append(0)
                        if method != 'IQR': sth_to_process = True
                    methods.append(method)
            
            if sth_to_process:
                # process removing outliers
                for i in range(len(cols)):
                    data, droped_val_nb = stats.remove_outliers(data,cols[i],methods[i],values[i])
                    droped_values_nb += droped_val_nb

                data.to_sql('uploaded_data', db_connector, if_exists='replace', index=False)

            db_connector.close()

            flash(f'Succesfully removed {droped_values_nb} rows as outliers.', category='info')
            return redirect(url_for('views.visualization_and_reporting'))

        except ValueError:
            flash('Input error! Pleas check writen values in text boxes.', category='error')

    db_connector.close()

    graphJSONtable = []
    colours = ['red', 'blue', 'orange', 'green', 'purple']
    for i in range(len(cols)):
        id = i%5
        graphJSON = reportGeneratorFunction.singleBoxPlot(data,cols[i],cols[i],[colours[id]])
        graphJSONtable.append(graphJSON)

    return render_template('outliers.html',
                            columns=cols,
                            len=len(cols),
                            graphJSONtable=graphJSONtable,
                            chartsQuantity = len(graphJSONtable))