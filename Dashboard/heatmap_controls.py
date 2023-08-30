"""
will have a bunch of different lists of option
serve on demand
by calling functions and telling them where you are in the decision tree
pass in the handles of these widgets directly?
these should be updated on each update
my brain is undergoing spontaneous combustion no
"""

from bokeh.io import curdoc
from bokeh.models import *
from bokeh.plotting import *
from bokeh.transform import linear_cmap
from bokeh.layouts import column, row
from utilities import heatmap_palette
from datetime import datetime, timedelta

from params import *

class HeatmapControls:

    def __init__(self, index, update_graph):
        self.index = index
        self.update_graph = update_graph
        self.changed = False
        self.status = {}

        # initializing graph control widgets

        self.title = TextInput(
            title='Title',
            value='Heatmap'
        )
        self.title.on_change('value', self.general_change_handler)

        self.scope = Select(
            title='Scope', 
            value='All', 
            options=['All', 'Sector', 'Asset']
        )
        self.scope.on_change('value', self.scope_handler)
        
        self.group_sector = Select(
            title='Group', 
            value='Consumer Discretionary', 
            options=sectors, 
            visible=False
        )
        self.group_sector.on_change('value', self.general_change_handler)
        
        self.group_ticker = AutocompleteInput(
            title='Group', 
            placeholder='Input name of the asset...', 
            completions=tickers, 
            search_strategy='includes', 
            visible=False
        )
        self.group_ticker.on_change('value', self.general_change_handler)

        self.group_var = Select(
            title='Group Variable', 
            value='Asset', 
            options=['Asset', 'Asset and score type']
        )
        self.group_var.on_change('value', self.group_var_handler)

        self.size_var = Select(
            title='Size Variable', 
            value='Buzz', 
            options=score_types
        )
        self.size_var.on_change('value', self.general_change_handler)

        self.size_checkbox = CheckboxGroup(
            labels=['Assign size by magnitude of deviation from mean'],
            active=[]
        )

        self.size_mean = Div(
            text='<p>Sample mean from a range of: </p>'
        )

        self.size_mean_range = NumericInput(
            value=30,
            low=1,
            width=50
        )

        self.size_mean_unit = Select(
            value='days',
            options=['days','months','years']
        )

        self.color_var = Select(
            title='Color Variable', 
            value='ESG Overall Score', 
            options=score_types
        )
        self.color_var.on_change('value', self.general_change_handler)

        self.color_checkbox = CheckboxGroup(
            labels=['Assign color by relative deviation from mean'],
            active=[]
        )

        self.color_mean = Div(
            text='<div>Sample mean from the past: </div>'
        )

        self.color_mean_range = NumericInput(
            value=30,
            low=1,
            width=50
        )

        self.color_mean_unit = Select(
            value='days',
            options=['days','months','years']
        )
        
        # TODO: impose selection logic



        self.update = Button(disabled=True, label='Show Results')
        self.update.on_click(self.update_handler)

        self.controls = column(
            self.title,
            row(self.scope, self.group_sector, self.group_ticker), 
            self.group_var, 
            self.size_var, 
            self.size_checkbox,
            self.size_mean,
            row(self.size_mean_range, self.size_mean_unit),
            self.color_var, 
            self.color_checkbox,
            self.color_mean,
            row(self.color_mean_range, self.color_mean_unit),
            self.update
        )
        pass

    def general_change_handler(self, attr, old, new):
        self.update.disabled = False
        pass

    def scope_handler(self, attr, old, new):
        self.update.disabled = False

        match new:
            case 'All':
                self.group_sector.visible = False
                self.group_ticker.visible = False
                self.group_var.value = 'Sector'
                self.group_var.options = ['Asset','Asset and score type']
                self.color_var.value = 'ESG Overall Score'
                self.color_var.options = score_types
                self.color_var.disabled = False
                self.color_checkbox.disabled = False

            case 'Sector':
                self.group_sector.visible = True
                self.group_ticker.visible = False
                self.group_var.value = 'Asset'
                self.group_var.options = ['Asset','Asset and score type']
                self.color_var.value = 'ESG Overall Score'
                self.color_var.options = score_types
                self.color_var.disabled = False
                self.color_checkbox.disabled = False

            case 'Asset':
                self.group_sector.visible = False
                self.group_ticker.visible = True
                self.group_var.value = 'Score type'
                self.group_var.options = ['Score type']
                self.color_var.value = '-'
                self.color_var.options = ['-']
                self.color_var.disabled = True
                self.color_checkbox.active = []
                self.color_checkbox.disabled = True
        pass

    def group_var_handler(self, attr, old, new):
        self.update.disabled = False

        match new:
            case 'Asset':
                self.color_var.value = 'ESG Overall Score'
                self.color_var.options = score_types
                self.color_var.disabled = False
                self.color_checkbox.disabled = False

            case 'Asset and score type':
                self.color_var.value = '-'
                self.color_var.options = ['-']
                self.color_var.disabled = True
                self.color_checkbox.active = []
                self.color_checkbox.disabled = True
        pass


    def update_handler(self):
        # potentially susceptible to code injection when rendering title without sanitizing user input!
        self.update_graph(self.get_status())
        self.update.disabled = True
        pass

    def get_controls(self):
        return self.controls
        pass

    def get_status(self):
        """
        This method collects all the control data into a single dictionary
        so it's easier to pass around
        """
        status = {}
        status['title'] = self.title.value
        status['scope'] = self.scope.value
        status['group_sector'] = self.group_sector.value
        status['group_ticker'] = self.group_ticker.value
        status['group_var'] = self.group_var.value
        status['color_var'] = self.color_var.value

        return status
        pass
