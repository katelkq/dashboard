import pandas as pd
from bokeh.io import curdoc
from bokeh.models import *
from bokeh.plotting import *
from bokeh.transform import linear_cmap
from utilities import *
from datetime import datetime, timedelta
from controls import Controls
import numpy as np
from params import *
from graph import Graph

API_KEY = 'rf_1nMfaWdyWfpmtWB9dRE'
DEBUG = False

class Heatmap(Graph):
    """
    A Graph object takes in a pandas dataframe
    the complete one, just so it can be adjusted as wished
    a couple of parameters for these adjustments
    the heatmap figure itself, along with control widgets
    two separate getter methods to return their handles?
    self.plot and self.controls (self.type?)
    preprocessing to derive heatmap related metrics (not needed for timeseries)
    """

    def __init__(self, update_main):
        self.index = 1
        self.type = 'heatmap'
        self.controls = Controls(1, self.update)
        self.update_main = update_main
        self.control_status = self.controls.get_status()

        self.fetch_data()
        self.preprocess()
        self.render()
        pass


    def update(self, control_status):
        if DEBUG:
            for (key, value) in control_status.items():
                print(f'Key: {key}, value: {value}, type: {type(value)}')

        self.control_status = control_status

        match control_status['type_of_graph']:
            case 'Heatmap':
                self.preprocess()
                self.render()

            case 'Timeseries':
                self.preprocess_timeseries()
                self.render_timeseries()

        self.update_main(self.index)
        pass

    def fetch_data(self):
        print(self.control_status['color_var'])

        if True or self.control_status['color_var'] in equcor_datacols['name']:
            print('Fetching!')

            start_date = self.control_status['start']
            end_date = self.control_status['end']

            url = f'https://dataapi.marketpsych.com/esg/v4/data/equcor/dai/all?apikey={API_KEY}&start_date={start_date}&end_date={end_date}&datacols=buzz,ESG&format=csv'
            print(url)

            self.source = pd.read_csv(url)
        pass

    def preprocess(self):
        self.source = self.source.drop_duplicates().sort_values(by=['buzz'], ascending=False).reset_index(drop=True).head(10)

        self.source['buzz_normalized'] = self.source['buzz'].divide(self.source['buzz'].sum())
        self.source['buzz_cumulative'] = self.source['buzz_normalized'].cumsum()

        # let's use 3 columns for this one
        cutoff1 = (self.source['buzz_cumulative']-1/3).abs().argsort()[:1][0]
        cutoff2 = (self.source['buzz_cumulative']-2/3).abs().argsort()[:1][0]

        # can look at the logic here if time
        first = self.source['buzz_cumulative'][cutoff1]
        second = self.source['buzz_cumulative'][cutoff2] - first
        third = 1 - first - second

        self.source.loc[:cutoff1, 'width'] = first
        self.source.loc[cutoff1+1:cutoff2, 'width'] = second
        self.source.loc[cutoff2+1:, 'width'] = third

        self.source['height'] = self.source['buzz_normalized'].divide(self.source['width'])

        self.source.loc[:cutoff1, 'x'] = 0
        self.source.loc[cutoff1+1:cutoff2, 'x'] = first
        self.source.loc[cutoff2+1:, 'x'] = first + second

        self.source.loc[:cutoff1, 'y'] = -self.source.loc[:cutoff1, 'height'].cumsum()

        self.source.loc[cutoff1+1:cutoff2, 'y'] = -self.source.loc[cutoff1+1:cutoff2, 'height'].cumsum()
        self.source.loc[cutoff2+1:, 'y'] = -self.source.loc[cutoff2+1:, 'height'].cumsum()

        self.source['label_y'] = self.source['y'] + self.source['height']

        print(self.source)
        pass

    def render(self):
        self.plot = figure(
            title=f'Graph #{self.index}',
            tools=[HoverTool(),SaveTool()],
            tooltips=[
                ('Name', '@name'),
                ('Buzz', '@buzz'),
                ('ESG Score', '@ESG')
            ],
            width=700,
            height=900
        )

        # add multiple renderers
        self.plot.block(
            x='x',
            y='y',
            width='width',
            height='height',
            line_color='white',
            line_width=5,
            fill_color=linear_cmap('ESG', heatmap_palette, 0, 100),
            source=ColumnDataSource(self.source))

        # customizing the plot
        self.plot.axis.visible = False
        self.plot.toolbar.logo = None
        self.plot.grid.grid_line_color = None

        # adding a color bar
        color_mapper = LinearColorMapper(palette=heatmap_palette, low=0, high=100)
        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12)

        labels_name = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-25, text='name', text_color='white', source=ColumnDataSource(self.source.loc[self.source['height']>0.1]))
        labels_ticker = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-40, text='ticker', text_color='yellow', source=ColumnDataSource(self.source.loc[self.source['height']>0.1]))
        labels_buzz = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-55, text='buzz', text_color='white', source=ColumnDataSource(self.source.loc[self.source['height']>0.1]))
        labels_esg = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-70, text='ESG', text_color='white', source=ColumnDataSource(self.source.loc[self.source['height']>0.1]))

        self.plot.add_layout(color_bar, 'right')
        self.plot.add_layout(labels_name)
        self.plot.add_layout(labels_ticker)
        self.plot.add_layout(labels_buzz)
        self.plot.add_layout(labels_esg)

        if self.control_status is not None:
            self.plot.title = self.control_status['title']

        pass

    def get_controls(self):
        return self.controls.get_controls()
        pass

    def get_plot(self):
        return self.plot
        pass