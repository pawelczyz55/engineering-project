from flask import Blueprint, flash, render_template, request, jsonify, url_for, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from .views import views

importCsv = Blueprint('import_csv', __name__)

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# w tej funkcji zmieńcie sobie scieżkę. Docelowo bedzie to zrobione tak, żeby oczywiscie sciezki w kodzie nie trzeba bylo zmieniac.
@importCsv.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = f'pnewFile.csv'
            #new_filename = f'{filename.split(".")[0]}_newfile.csv'
            save_location = os.path.join('C:\py\proj_inz\engineering-project\csv_data', new_filename.replace('\\', ''))
            file.save(save_location)

        return redirect(url_for('views.visualization_and_reporting'))

    return render_template('upload.html',user=current_user)