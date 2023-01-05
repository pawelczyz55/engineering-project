from flask_wtf import FlaskForm
from wtforms import SelectField

class Forms(FlaskForm):
    chartType = SelectField("chartType", choices=[('barplot', 'Bar Plot'), ('scatterplot', 'Scatter Plot')])
    #modes = SelectField("mode", choices=[()])
