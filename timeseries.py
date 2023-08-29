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

API_KEY = 'rf_1nMfaWdyWfpmtWB9dRE'
DEBUG = False

class TimeSeries(Graph):
    """
    A Graph object takes in a pandas dataframe
    the complete one, just so it can be adjusted as wished
    a couple of parameters for these adjustments
    the heatmap figure itself, along with control widgets
    two separate getter methods to return their handles?
    self.plot and self.controls (self.type?)
    preprocessing to derive heatmap related metrics (not needed for timeseries)
    """

    def __init__(self, index, update_main):
        self.index = index
        self.type = 'heatmap'
        self.controls = Controls(index, self.update)
        self.update_main = update_main
        self.control_status = self.controls.get_status()

        self.import_data()
        self.preprocess_heatmap()
        self.render_heatmap()
        pass

    def update(self, control_status):
        if DEBUG:
            for (key, value) in control_status.items():
                print(f'Key: {key}, value: {value}, type: {type(value)}')

        self.control_status = control_status

        match control_status['type_of_graph']:
            case 'Heatmap':
                self.preprocess_heatmap()
                self.render_heatmap()

            case 'Timeseries':
                self.preprocess_timeseries()
                self.render_timeseries()

        self.update_main(self.index)
        pass

    def import_data(self):
        print(self.control_status['color_var'])

        if True or self.control_status['color_var'] in equcor_datacols['name']:
            print('Fetching!')

            start_date = self.control_status['start']
            end_date = self.control_status['end']

            url = f'https://dataapi.marketpsych.com/esg/v4/data/equcor/dai/all?apikey={API_KEY}&start_date={start_date}&end_date={end_date}&datacols=buzz,ESG&format=csv'
            print(url)

            self.source = pd.read_csv(url)


        pass

    def preprocess_timeseries(self):
        self.source = pd.read_csv('./Dashboard/sample_data/4295905573.csv')
        self.source = pd.concat([self.source]*5, ignore_index=True)

        delta = np.repeat(np.arange(0,5),4)
        self.source['windowTimestamp'] = pd.to_datetime(self.source['windowTimestamp']) + pd.to_timedelta(delta, unit='day')
        nums = list(self.source.columns)[6:]
        self.source[nums] = self.source[nums].apply(lambda x: np.random.normal(loc=x, scale=0.2*np.abs(x)))
        pass

    def render_timeseries(self):

        # create a new plot with a title and axis labels
        self.plot = figure(
            title="Timeseries example",
            x_axis_label="Time",
            x_axis_type='datetime',
            y_axis_label="Management Sentiment",
            toolbar_location = "above",
            tools=[HoverTool()],
            tooltips="(@x,@y)"
        )

        # add renderers
        self.plot.line(self.source.loc[self.source['dataType'] == 'News', 'windowTimestamp'], self.source.loc[self.source['dataType'] == 'News', 'managementSentiment'], legend_label="News", color="steelblue", line_width=2)
        self.plot.circle(self.source.loc[self.source['dataType'] == 'News', 'windowTimestamp'], self.source.loc[self.source['dataType'] == 'News', 'managementSentiment'], color="steelblue", size=5)
        self.plot.line(self.source.loc[self.source['dataType'] == 'News_Headline', 'windowTimestamp'], self.source.loc[self.source['dataType'] == 'News_Headline', 'managementSentiment'], legend_label="News_Headline", color="pink", line_width=2)
        self.plot.circle(self.source.loc[self.source['dataType'] == 'News_Headline', 'windowTimestamp'], self.source.loc[self.source['dataType'] == 'News_Headline', 'managementSentiment'], color="pink", size=5)
        self.plot.line(self.source.loc[self.source['dataType'] == 'News_Social', 'windowTimestamp'], self.source.loc[self.source['dataType'] == 'News_Social', 'managementSentiment'], legend_label="News_Social", color="magenta", line_width=2)
        self.plot.circle(self.source.loc[self.source['dataType'] == 'News_Social', 'windowTimestamp'], self.source.loc[self.source['dataType'] == 'News_Social', 'managementSentiment'], color="magenta", size=5)
        self.plot.line(self.source.loc[self.source['dataType'] == 'Social', 'windowTimestamp'], self.source.loc[self.source['dataType'] == 'Social', 'managementSentiment'], legend_label="Social", color="lime", line_width=2)
        self.plot.circle(self.source.loc[self.source['dataType'] == 'Social', 'windowTimestamp'], self.source.loc[self.source['dataType'] == 'Social', 'managementSentiment'], color="lime", size=5)

        # customizing the plot
        self.plot.toolbar.logo = None
        self.plot.yaxis.formatter = NumeralTickFormatter(format='0.00%')
        self.plot.legend.location = 'right'

        pass

    def get_controls(self):
        return self.controls.get_controls()
        pass

    def get_plot(self):
        return self.plot
        pass