from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Button, Select, Div, Tabs, TabPanel
from functools import partial
from sample_plot import SamplePlot
from graph import Graph
from heatmap import Heatmap

curdoc().title = "Dashboard"

# generating layout components
# title and description
header = Div(
    text='''
        <header>
            <h1>Title</h1>
            <p>Some descriptions as to how this might be used...</p>
        </header>
        ''',
    sizing_mode='stretch_width'
)

def update():
    graph_area.children = graph.get_plot()
    pass

# initializing layout
control_panel = Tabs(tabs=[])
control_area = column(header, control_panel)

graph = Heatmap(update_main=update)

graph_area = column(row(graph.get_plot()), width_policy='max')

control_panel.tabs.append(TabPanel(title='Heatmap', child=graph.get_controls()))
control_panel.tabs.append(TabPanel(title='Time Series', child=graph.get_controls()))

layout = row(control_area, graph_area)

curdoc().add_root(layout)

