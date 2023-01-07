from flask import Blueprint, flash, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from functions import statsCsv
from .models import Note
from . import db
import json
import os
import pandas as pd
import plotly
import plotly.express as px

from functions.importCsvData import procces_csv

test = Blueprint('test', __name__)

@test.route('/test', methods=['POST', 'GET'])
@login_required
def testowy():
    df = px.data.iris()
    stats = statsCsv.file_statistics(df)

    return render_template("testowy.html", stats)
