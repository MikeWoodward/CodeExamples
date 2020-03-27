# %%
# Imports
# =======
from os.path import dirname, join
import math
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (ColumnDataSource, DataTable,
                          NumberFormatter, RangeSlider, TableColumn,
                          HTMLTemplateFormatter)

# %%
# Main
# ====

# TODO There's a weakness here - if the user changes the column widths
# manually, text can be hidden. there should be a callback when column
# widths are changed that sets the row height in the same way the 
# update function does.

def update():
    
    """callback function when slider is changed. Dynamically adjusts row
    height."""
    
    current = df[(df['salary'] >= slider.value[0]) & 
                 (df['salary'] <= slider.value[1])].dropna()
    
    source.data = {
        'name'             : current.name,
        'salary'           : current.salary,
        'years_experience' : current.years_experience,
        'points'           : current.points,
        'commute_distance' : current.commute_distance,
        'fake_column'      : current.fake_column,
        'error_message'    : current.error_message,
        'end_column'       : current.end_column
    }
    
    # Find the maximum number of characters in an entry - we'll use this
    # in conjunction with the width of the column to set the height of the
    # row
    char_count = max(data_table.source.data['error_message'].str.len())

    # Find the width of the column
    column_width = [x for x in data_table.columns 
                    if x.name == "error_message"][0].width

    # 5 is cell padding, 20 is the height of a row, 7 is the average width
    # in pixels of a character, math.ceil(char_count*7/column_width) gives
    # the number of rows.
    # TODO Can't find way of finding font size and name for column
    data_table.row_height = 5 + 20*math.ceil(char_count*7/column_width)

df = pd.read_csv(join(dirname(__file__), 'salary_data.csv'))
source = ColumnDataSource(data=dict())

slider = RangeSlider(title="Max Salary", 
                     start=10000, end=110000, 
                     value=(10000, 110000), 
                     step=1000, 
                     format="0,0")

slider.on_change('value', lambda attr, old, new: update())

# HTML formatter code for error_message column. Makes the text in the column 
# wrap. 
# TODO if the text truncates, we should have an ellipsis to indicate this
# has happened, but I can't figure out how to do this right now.
text_wrap_template = \
    """<span style="overflow-wrap: normal; 
                    white-space: normal;">
        <%= value %></span>"""
text_wrap_formatter = HTMLTemplateFormatter(template=text_wrap_template)

columns = [
    TableColumn(field="name", 
                title="Employee Name",
                width=150),
    TableColumn(field="salary", 
                title="Income", 
                formatter=NumberFormatter(format="$0,0.00"),
                width=80),
    TableColumn(field="years_experience", 
                title="Experience (years)",
                width=150),
    TableColumn(field="points", 
                title="Points",
                formatter=NumberFormatter(format="0,0.00"),
                width=100),
    TableColumn(field="commute_distance", 
                title="Commuting distance",
                formatter=NumberFormatter(format="0,0.00"),
                width=160),
    TableColumn(field="fake_column", 
                title="Fake column",
                formatter=NumberFormatter(format="0,0.00"),
                width=120),
    # Note that this column is named - we use the column name to work out
    # the column width later
    TableColumn(field="error_message", 
                title="Error message",
                name="error_message",
                formatter=text_wrap_formatter,
                width=100),
    TableColumn(field="end_column", 
                title="end column",
                width=80)
]

# Note two things here:
# We set fit_columns True which means the columns are forcibly fit to 800 
# pixels
# The column widths from the columns variable add up to more than 800, so
# they're treated as a maximum width - another reason why we need to get the
# column width in the callback function
data_table = DataTable(source=source, 
                       columns=columns, 
                       editable=False,
                       index_position=None,
                       fit_columns=True,
                       width=800)

controls = column(slider)

curdoc().add_root(row(controls, data_table))
curdoc().title = "TableRowHeight"

update()
