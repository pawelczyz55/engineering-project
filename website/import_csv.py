from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user
from . import db
import pandas as pd
from sqlalchemy import exc

importCsv = Blueprint('import_csv', __name__)

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename: str) -> bool: 
    """
    Check if given file has allowed extention

    Parameters:
        - filename: string - name of the file 

    Returns:
        - bool - True/False 
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@importCsv.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # Load data from page
        sep = request.form.get('separator')
        if sep=='': sep=';'
        file = request.files['file']

        # If file extention is acceptable
        if file and allowed_file(file.filename):
            # Read file to pandas
            if request.form.get('if_use_first_row_as_column')!='on':
                data = pd.read_csv(file,header=None, sep=sep)
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
                # If error while file uploading or loading to data base print 'Having trouble' page
                return render_template("visualization_and_reporting.html",user=current_user, dataFound = False)

        # If correctly uploaded go to rename column page 
        return redirect(url_for('views.rename_columns'))

    # Render '/upload' page
    return render_template('upload.html',user=current_user)