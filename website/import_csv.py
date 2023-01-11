from flask import Blueprint, flash, render_template, request, jsonify, url_for, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from .views import views
from . import db
import pandas as pd
from sqlalchemy import exc
import csv

importCsv = Blueprint('import_csv', __name__)

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@importCsv.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Read file to pandas
            if request.form.get('if_use_first_row_as_column')!='on':
                data = pd.read_csv(file,header=None, sep=';')
                data.columns = [f'column {i}' for i in range(1,data.shape[1]+1)]
            else:
                data = pd.read_csv(file)
            
            # Write data into the table in SQLite database
            try:
                engine = db.get_engine()
                connnection = engine.connect()
                data.to_sql('test', connnection, if_exists='replace', index=False)
                connnection.close()
            except (exc.ArgumentError, exc.DatabaseError):
                 pass
            

        return redirect(url_for('views.visualization_and_reporting'))

    return render_template('upload.html',user=current_user)