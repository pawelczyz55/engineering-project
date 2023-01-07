from flask_wtf import FlaskForm
from wtforms import SelectField

class Forms(FlaskForm):
    chartType = SelectField("chartType", choices=[('barplot', 'Bar Plot'), ('scatterplot', 'Scatter Plot'),
    ('piechartplot', 'Pie Chart'),('lineplot', 'Line Plot'), ('lineareaplot', 'Area Plot'),('histogramplot', 'Histogram'),
    ('boxplot', 'Box Plot'),('violinplot', 'Violin Plot'),('heatmapplot', 'Heatmap')])
    #modes = SelectField("mode", choices=[()])
