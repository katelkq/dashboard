from bokeh.models import *
from bokeh.plotting import *
from utilities import *

import numpy as np
import pandas as pd

from api import API_KEY
from graph import Graph
from timeseries_controls import TimeSeriesControls
from params import *

DEBUG = False

class TimeSeries(Graph):
    """
    Inherits from :ref:`Graph <graph>`. It's API handling and data processing and graphing all in one.

    """

    def init_controls(self):
        self.controls = TimeSeriesControls(self.update)
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

        self.update_main('Timeseries')
        pass

    def fetch_data(self):
        # asset code, variable, date range
        url = f"https://dataapi.marketpsych.com/esg/v4/data/equcor/dai/{self.control_status['asset']}?apikey={API_KEY}&start_date={self.control_status['start_date']}&end_date={self.control_status['end_date']}&datacols={self.control_status['var']}&format=csv"

        if DEBUG: print(url)

        self.source = pd.read_csv(url)
        self.source['windowTimestamp'] = pd.to_datetime(self.source['windowTimestamp'])

        if DEBUG: # prints the data as freshly fetched from Refinitiv
            print(self.source)
        pass

    def preprocess(self):
        if self.control_status['mean_checkbox']:
            var = self.control_status['var']
            days = self.control_status['mean_days']

            self.source[f'{var}_{days}d_mean'] = self.source.rolling(days)[var].mean()
            self.source[f'{var}_{days}d_std'] = self.source.rolling(days)[var].std()

            self.outliers = self.source.loc[(self.source[var] - self.source[f'{var}_{days}d_mean']).abs() > self.control_status['std'] * self.source[f'{var}_{days}d_std']]

        pass

    def render(self):
        var = self.control_status['var']

        # create a new plot with a title and axis labels
        self.plot = figure(
            title='Time Series',
            x_axis_type='datetime',
            y_range=(self.source[var].min() * 0.9, self.source[var].max() * 1.1),
            tools=[HoverTool(
                tooltips=[
                    ('Date', '@windowTimestamp{%F}'),
                    (var, f'@{var}')
                ],
                formatters={'@windowTimestamp': 'datetime'}),SaveTool()],
            
            width=1400,
            height=900
        )

        # add renderers
        self.plot.vbar(
            x='windowTimestamp',
            top=var,
            source=ColumnDataSource(self.source)
        )

        # add highlights
        if self.control_status['mean_checkbox']:
            self.plot.vbar(
                x='windowTimestamp',
                top=var,
                color='lime',
                source=ColumnDataSource(self.outliers)
            )

        self.plot.line(
            x='windowTimestamp',
            y=var,
            legend_label=var,
            line_width=2,
            source=ColumnDataSource(self.source)
        )

        # customizing the plot
        self.plot.toolbar.logo = None

        pass

    def get_controls(self):
        return self.controls.get_controls()
        pass

    def get_plot(self):
        return self.plot
        pass

    def activate_update(self):
        """
        Make the `Show Results` button clickable again!
        
        """

        self.controls.update.disabled = False
        pass
