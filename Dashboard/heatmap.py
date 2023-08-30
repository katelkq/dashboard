import pandas as pd
from bokeh.io import curdoc
from bokeh.models import *
from bokeh.plotting import *
from bokeh.transform import linear_cmap
from utilities import *
from datetime import datetime, timedelta
from heatmap_controls import HeatmapControls
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

    def init_controls(self):
        self.controls = HeatmapControls(self.update)
        self.control_status = self.controls.get_status()
        pass

    def update(self):
        self.control_status = self.controls.get_status()

        if DEBUG: # prints the items in control_status
            for (key, value) in self.control_status.items():
                print(f'Key: {key}, value: {value}, type: {type(value)}')

        self.fetch_data()
        self.preprocess()
        self.render()

        self.update_main('Heatmap')
        pass

    def fetch_data(self):
        start_date = min(self.control_status['size_mean_start'], self.control_status['color_mean_start'])
        end_date = max(self.control_status['size_mean_end'], self.control_status['color_mean_end'])
        url = f"https://dataapi.marketpsych.com/esg/v4/data/equcor/dai/all?apikey={API_KEY}&start_date={start_date}&end_date={end_date}&datacols={self.control_status['size_var']},{self.control_status['color_var']}&format=csv"

        if DEBUG: print(url)
        self.source = pd.read_csv(url)

        if DEBUG: # prints the data as freshly fetched from Refinitiv
            print(self.source)
        pass

    def preprocess(self):
        """
        some logic to derive heatmap related rendering metrics
        """
        # to preserve levels of sanity
        size = self.control_status['size_var']
        color = self.control_status['color_var']


        # x is the number of entities displayed in the heatmap
        x = 20

        self.source = self.source.drop_duplicates().sort_values(by=[size], ascending=False).reset_index(drop=True).head(x)

        self.source[f'{size}_normalized'] = self.source[size].divide(self.source[size].sum())
        self.source[f'{size}_cumulative'] = self.source[f'{size}_normalized'].cumsum()

        # n is the number of columns displayed in the heatmap
        n = 4

        cutoff_indices = []
        for i in range(n):
            cutoff_indices.append((self.source[f'{size}_cumulative'] - (i+1)/n).abs().argsort()[:1][0])

        # slightly twisted logic
        cutoff_widths = [self.source[f'{size}_cumulative'][cutoff_indices[0]]]
        for i in range(1, n):
            width = self.source[f'{size}_cumulative'][cutoff_indices[i]] - sum(cutoff_widths)
            cutoff_widths.append(width)

        cutoff_indices.insert(0, -1)
        cutoff_indices.append(len(self.source)-1)
        
        for i in range(n):
            self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'width'] = cutoff_widths[i]
            self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'x'] = sum(cutoff_widths[:i])

        self.source['height'] = self.source[f'{size}_normalized'].divide(self.source['width'])
        
        for i in range(n):
            self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'y'] = -self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'height'].cumsum()

        self.source['label_y'] = self.source['y'] + self.source['height']

        if DEBUG: print(self.source)
        pass

    def render(self):
        self.plot = figure(
            title='Heatmap',
            tools=[HoverTool(),SaveTool()],
            tooltips=[
                ('Name', '@name'),
                (self.control_status['size_var'], f"@{self.control_status['size_var']}"),
                (self.control_status['color_var'], f"@{self.control_status['color_var']}")
            ],
            width=1400,
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
            fill_color=linear_cmap(self.control_status['color_var'], heatmap_palette, 0, 100),
            source=ColumnDataSource(self.source))

        # customizing the plot
        self.plot.axis.visible = False
        self.plot.toolbar.logo = None
        self.plot.grid.grid_line_color = None

        # adding a color bar
        # TODO: low and high needs adjustment with variable
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