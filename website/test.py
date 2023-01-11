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
       if request.method == 'POST':
              xs = request.form.getlist('x[]')
              print(xs)
              ys = request.form.getlist('y[]')
              print(ys)
              colors = request.form.getlist('color[]')
              print(colors)
              return render_template("testowyraport.html",user=current_user, x = xs, y=ys, colors=colors)

#     df = px.data.iris()
#     fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", marginal_y="violin",
#            marginal_x="box", trendline="ols", template="simple_white")

#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
       return render_template("testowy.html",user=current_user)
