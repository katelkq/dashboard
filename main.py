from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Button, Select, Div, Tabs, TabPanel
from functools import partial
from sample_plot import SamplePlot
from graph import Graph

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

# control element for the number of plots on display
num_of_plots = Select(title='Choose the number of plots on display: ', value='1', options=['1','2'])

def num_of_plots_handler(attr, old, new):
    if old == new:
        return
    old, new = int(old), int(new)
    # unsure as to whether directly modifying the children field is safe practice
    # nevertheless it seems to work as intended
    if old < new:
        while old < new:
            graphs.append(Graph(index=old+1, update_main=update))
            graph_area.children[old//2].children.append(graphs[-1].get_plot())
            control_panel.tabs.append(TabPanel(title=f'Graph #{old+1}', child=(graphs[-1].get_controls())))
            old += 1
    else:
        while old > new:
            old -= 1
            graphs.pop()
            graph_area.children[old//2].children.pop()
            control_panel.children.pop()

    pass

num_of_plots.on_change('value', num_of_plots_handler)


def update(index):
    match index:
        case 1:
            graph_area.children[0].children[0] = graphs[0].get_plot()
        case 2:
            graph_area.children[0].children[1] = graphs[1].get_plot()
        case 3:
            graph_area.children[1].children[0] = graphs[2].get_plot()
        case 4:
            graph_area.children[1].children[1] = graphs[3].get_plot()
    pass

subheader = Div(
    text='<h3>Control Panel</h3>'
)

# initializing layout
control_panel = Tabs(tabs=[])
control_area = column(header, num_of_plots, subheader, control_panel)


graphs = [Graph(index=1, update_main=update)]

graph_area = column(row(graphs[0].get_plot()), width_policy='max')

control_panel.tabs.append(TabPanel(title='Graph #1', child=graphs[0].get_controls()))

layout = row(control_area, graph_area)

curdoc().add_root(layout)

