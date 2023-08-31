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

# TODO: get authentication stuff into a separate file
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
        # fetch as much as needed
        start_date = min(self.control_status['size_mean_start'], self.control_status['color_mean_start'])
        end_date = max(self.control_status['size_mean_end'], self.control_status['color_mean_end'])

        match self.control_status['scope']:
            case 'All':
                url = f"https://dataapi.marketpsych.com/esg/v4/data/equcor/dai/all?apikey={API_KEY}&start_date={start_date}&end_date={end_date}&datacols={self.control_status['size_var']},{self.control_status['color_var']}&format=csv"

            case 'Sector':
                url = f"https://dataapi.marketpsych.com/esg/v4/data/equcor/dai/all?apikey={API_KEY}&start_date={start_date}&end_date={end_date}&datacols={self.control_status['size_var']},{self.control_status['color_var']}&format=csv"

            case 'Asset':
                url = f"https://dataapi.marketpsych.com/esg/v4/data/equcor/dai/{self.control_status['asset_code']}?apikey={API_KEY}&start_date={start_date}&end_date={end_date}&format=csv"

        if DEBUG: # prints the assembled url
            print(url)

        # TODO: catch error and display error message
        self.source = pd.read_csv(url)

        if DEBUG: # prints the data as freshly fetched from Refinitiv
            print(self.source)
        pass

    def preprocess(self):
        """
        some logic to derive heatmap related rendering metrics
        warning: in no way is this thing optimized
        """
        # filter source if scope = Sector
        match self.control_status['scope']:
            case 'Sector':
                asset_codes = equcor_assets.loc[equcor_assets['TRBCEconomicSector'] == self.control_status['scope_sector'], 'assetCode'].to_csv(header=None, index=False).strip('\n').split('\n')
                asset_codes = set(map(int, asset_codes))
                
                self.source = self.source.loc[self.source['assetCode'].isin (asset_codes)]

        # name shortcuts for your sanity
        size_var = self.control_status['size_var']
        color_var = self.control_status['color_var']

        # heatmap preprocessing logic for scope = All or Sector
        # TODO: Sector can be extended to Asset-like logic w/ grouping option of asset + score type
        if self.control_status['scope'] == 'All' or self.control_status['scope'] == 'Sector':
            # x is the number of entities displayed in the heatmap
            x = 20

            self.source = self.source.drop_duplicates().sort_values(by=[size_var], ascending=False).reset_index(drop=True).head(x)

            self.source[f'{size_var}_normalized'] = self.source[size_var].divide(self.source[size_var].sum())
            self.source[f'{size_var}_cumulative'] = self.source[f'{size_var}_normalized'].cumsum()

            # n is the number of columns displayed in the heatmap
            n = 4

            cutoff_indices = []
            for i in range(n):
                cutoff_indices.append((self.source[f'{size_var}_cumulative'] - (i+1)/n).abs().argsort()[:1][0])

            # slightly twisted logic
            cutoff_widths = [self.source[f'{size_var}_cumulative'][cutoff_indices[0]]]
            for i in range(1, n):
                width = self.source[f'{size_var}_cumulative'][cutoff_indices[i]] - sum(cutoff_widths)
                cutoff_widths.append(width)

            cutoff_indices.insert(0, -1)
            cutoff_indices.append(len(self.source)-1)
            
            for i in range(n):
                self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'width'] = cutoff_widths[i]
                self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'x'] = sum(cutoff_widths[:i])

            self.source['height'] = self.source[f'{size_var}_normalized'].divide(self.source['width'])
            
            for i in range(n):
                self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'y'] = -self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'height'].cumsum()

            self.source['label_y'] = self.source['y'] + self.source['height']

        else:
            id_vars = list(self.source.columns)[:6]
            color_vars = list(self.source.columns)[7:]
            self.source = pd.melt(self.source, id_vars=id_vars, value_name='score')

            # kick out buzz because it's meaningless to display it alongside other scores in a heatmap
            self.source = self.source.loc[self.source['variable'] != 'buzz']
            
            # TODO: deviation from mean handler!!!
            # is it by score, or by abs of std?
            
            # see if the checkboxes are ticked
            if self.control_status['color_checkbox']:
                interval = self.control_status['color_mean_interval']

                for color_var in color_vars:
                    self.source.loc[self.source['variable'] == color_var, f'{interval}d_mean'] = self.source.loc[self.source['variable'] == color_var, 'score'].rolling(interval).mean()
                    self.source.loc[self.source['variable'] == color_var, f'{interval}d_std'] = self.source.loc[self.source['variable'] == color_var, 'score'].rolling(interval).std()

                self.source[f'{interval}d_distance'] = (self.source['score'] - self.source[f'{interval}d_mean']).div(self.source[f'{interval}d_std'])

            size_var = 'score'
            if self.control_status['size_checkbox']:
                interval = self.control_status['size_mean_interval']
                size_var = f'{interval}d_distance_abs'

                for color_var in color_vars:
                    self.source.loc[self.source['variable'] == color_var, f'{interval}d_mean'] = self.source.loc[self.source['variable'] == color_var, 'score'].rolling(interval).mean()
                    self.source.loc[self.source['variable'] == color_var, f'{interval}d_std'] = self.source.loc[self.source['variable'] == color_var, 'score'].rolling(interval).std()

                self.source[f'{interval}d_distance'] = (self.source['score'] - self.source[f'{interval}d_mean']).div(self.source[f'{interval}d_std'])
                self.source[f'{interval}d_distance_abs'] = self.source[f'{interval}d_distance'].abs()

            self.source = self.source.sort_values(by=[size_var], ascending=False).reset_index(drop=True)

            self.source[f'normalized'] = self.source[size_var].divide(self.source[size_var].sum())
            self.source[f'cumulative'] = self.source[f'normalized'].cumsum()

            # n is the number of columns displayed in the heatmap
            n = 4

            cutoff_indices = []
            for i in range(n):
                cutoff_indices.append((self.source[f'cumulative'] - (i+1)/n).abs().argsort()[:1][0])

            # slightly twisted logic
            cutoff_widths = [self.source[f'cumulative'][cutoff_indices[0]]]
            for i in range(1, n):
                width = self.source[f'cumulative'][cutoff_indices[i]] - sum(cutoff_widths)
                cutoff_widths.append(width)

            cutoff_indices.insert(0, -1)
            cutoff_indices.append(len(self.source)-1)
            
            for i in range(n):
                self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'width'] = cutoff_widths[i]
                self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'x'] = sum(cutoff_widths[:i])

            self.source['height'] = self.source[f'normalized'].divide(self.source['width'])
            
            for i in range(n):
                self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'y'] = -self.source.loc[cutoff_indices[i]+1:cutoff_indices[i+1], 'height'].cumsum()

            self.source['label_y'] = self.source['y'] + self.source['height']

        if DEBUG: # prints the preprocessed data
            print(self.source)
        pass

    def render(self):
        if self.control_status['scope'] == 'All' or self.control_status['scope'] == 'Sector':
            size_var = self.control_status['size_var']
            color_var = self.control_status['color_var']

            self.plot = figure(
                title='Heatmap',
                tools=[HoverTool(),SaveTool()],
                tooltips=[
                    ('Name', '@name'),
                    (size_var, f'@{size_var}'),
                    (color_var, f'@{color_var}')
                ],
                width=1400,
                height=900
            )

            # add multiple renderers
            if 'Controvers' in self.control_status['color_var']:
                colormap = linear_cmap(color_var, heatmap_palette_reversed, 0, 100)
            else:
                colormap = linear_cmap(color_var, heatmap_palette, 0, 100)

            self.plot.block(
                x='x',
                y='y',
                width='width',
                height='height',
                line_color='white',
                line_width=5,
                fill_color=colormap,
                source=ColumnDataSource(self.source))

            # customizing the plot
            self.plot.axis.visible = False
            self.plot.toolbar.logo = None
            self.plot.grid.grid_line_color = None

            # adding a color bar
            # TODO: low and high needs adjustment with each specific variable? (is this the case for Core variables, though?)
            if 'Controvers' in color_var:
                color_mapper = LinearColorMapper(palette=heatmap_palette_reversed, low=0, high=100)
            else:
                color_mapper = LinearColorMapper(palette=heatmap_palette, low=0, high=100)
            
            color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12)

            # a subset of the preprocessed data source, where the space is enough for textual labels
            source_full_labels = ColumnDataSource(self.source.loc[self.source['height'] > 0.1])

            labels_name = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-25, text='name', text_color='white', source=source_full_labels)
            labels_ticker = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-40, text='ticker', text_color='yellow', source=source_full_labels)
            labels_buzz = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-55, text=size_var, text_color='white', source=source_full_labels)
            labels_score = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-70, text=color_var, text_color='white', source=source_full_labels)

            self.plot.add_layout(color_bar, 'right')
            self.plot.add_layout(labels_name)
            self.plot.add_layout(labels_ticker)
            self.plot.add_layout(labels_buzz)
            self.plot.add_layout(labels_score)

            self.plot.title = self.control_status['title']

        else:
            tooltips=[
                ('Name', '@name'),
                ('Score type', '@variable'),
                ('Value', '@score')
            ]

            if self.control_status['size_checkbox']:
                interval = self.control_status['size_mean_interval']
                tooltips.append((f'{interval}d_distance', f'@{interval}d_distance'))

            color_var = 'score'
            if self.control_status['color_checkbox']:
                interval = self.control_status['color_mean_interval']
                color_var = f'{interval}d_distance'
                tooltips.append((f'{interval}d_distance', f'@{interval}d_distance'))
            
            self.plot = figure(
                title='Heatmap',
                tools=[HoverTool(),SaveTool()],
                tooltips=tooltips,
                width=1400,
                height=900
            )

            # add multiple renderers
            # TODO: controversy variables need reversed color
            match color_var:
                case 'score':
                    colormap = linear_cmap(color_var, heatmap_palette, 0, 100)

                    # adding a color bar
                    # TODO: low and high needs adjustment with variable...?
                    color_mapper = LinearColorMapper(palette=heatmap_palette, low=0, high=100)
                    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12)

                case _:
                    colormap = linear_cmap(color_var, heatmap_palette, -5, 5)

                    # adding a color bar
                    # TODO: low and high needs adjustment with variable...?
                    color_mapper = LinearColorMapper(palette=heatmap_palette, low=-5, high=5)
                    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12)


            self.plot.block(
                x='x',
                y='y',
                width='width',
                height='height',
                line_color='white',
                line_width=5,
                fill_color=colormap,
                source=ColumnDataSource(self.source))

            # customizing the plot
            self.plot.axis.visible = False
            self.plot.toolbar.logo = None
            self.plot.grid.grid_line_color = None

            

            labels_name = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-25, text='name', text_color='white', source=ColumnDataSource(self.source.loc[self.source['height']>0.1]))
            labels_ticker = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-40, text='ticker', text_color='yellow', source=ColumnDataSource(self.source.loc[self.source['height']>0.1]))
            labels_variable = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-55, text='variable', text_color='white', source=ColumnDataSource(self.source.loc[self.source['height']>0.1]))
            labels_score = LabelSet(x='x', y='label_y', x_offset=10, y_offset=-70, text='score', text_color='white', source=ColumnDataSource(self.source.loc[self.source['height']>0.1]))

            self.plot.add_layout(color_bar, 'right')
            self.plot.add_layout(labels_name)
            self.plot.add_layout(labels_ticker)
            self.plot.add_layout(labels_variable)
            self.plot.add_layout(labels_score)

            self.plot.title = self.control_status['title']
        pass

    def get_controls(self):
        return self.controls.get_controls()
        pass

    def get_plot(self):
        return self.plot
        pass

    def activate_update(self):
        self.controls.update.disabled = False
        pass
