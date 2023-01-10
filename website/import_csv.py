from flask import Blueprint, flash, render_template, request, jsonify, url_for, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from .views import views
from . import db, db_connector
from pandas import read_csv

importCsv = Blueprint('import_csv', __name__)

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def table_exist(file_name: str):


@importCsv.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = f'pnewFile.csv'
            #save_location = f'csv_data\{new_filename}'
            save_location = f'csv_data\\{new_filename}'.replace('\\', '')
            #new_filename = f'{filename.split(".")[0]}_newfile.csv'
            #save_location = os.path.join('csv_data', new_filename.replace('\\', '\'))
            #file.save(save_location)
            file.save(r'C:\Users\mjurc\OneDrive\Pulpit\engineering-project\csv_data\pnewFile.csv')


            # Read data from CSV and load into a dataframe object
            tmp = request.form.get('if_use_first_row_as_column')
            if request.form.get('if_use_first_row_as_column')!='on':
                #col_nb = pd.read_csv(file, nrows=1).shape[1]
                cols2 = read_csv(r'C:\Users\mjurc\OneDrive\Pulpit\engineering-project\csv_data\pnewFile.csv', nrows=1, sep=';')
                col_nb = cols2.shape[1]
                columns = [f'column {i}' for i in range(1,col_nb+1)]
                #data = read_csv(file, names=columns)
                data = read_csv(r'C:\Users\mjurc\OneDrive\Pulpit\engineering-project\csv_data\pnewFile.csv', names=columns, sep=';')
            else:
                #data = read_csv(file)
                data = read_csv(r'C:\Users\mjurc\OneDrive\Pulpit\engineering-project\csv_data\pnewFile.csv')
            
            # Write data into the table in PostgreSQL database
            data.to_sql('test', db_connector)

        return redirect(url_for('views.visualization_and_reporting'))

    return render_template('upload.html',user=current_user)