from flask_wtf import FlaskForm
from wtforms import SelectField

class ChartType(FlaskForm):
    chartType = SelectField("chartType", choices=[('barplot', 'Bar Plot'), ('scatterplot', 'Scatter Plot')])