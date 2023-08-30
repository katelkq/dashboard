from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Button, Select, Div, Tabs, TabPanel
from functools import partial
from heatmap import Heatmap
from timeseries import TimeSeries

curdoc().title = "Dashboard"

# generating layout components
# title and description
header = Div(
    text='''
        <header>
            <h1>Dashboard</h1>
            <p>Some suggestions as to how this might be used...</p>
        </header>
        ''',
    sizing_mode='stretch_width'
)

def update(display):
    """
    """
    match display:
        case 'Heatmap':
            layout.children[1] = heatmap.get_plot()

        case 'Timeseries':
            layout.children[1] = timeseries.get_plot()
    
    pass

# initializing control area layout
control_panel = Tabs(tabs=[])
control_area = column(header, control_panel, width=400)

heatmap = Heatmap(update_main=update)
timeseries = TimeSeries(update_main=update)

# adding graph controls to the control panel
control_panel.tabs.append(TabPanel(title='Heatmap', child=heatmap.get_controls()))
control_panel.tabs.append(TabPanel(title='Time Series', child=timeseries.get_controls()))

layout = row(control_area, heatmap.get_plot())

curdoc().add_root(layout)

