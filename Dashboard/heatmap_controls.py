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
from bokeh.models.dom import HTML

from params import *

class HeatmapControls:

    def __init__(self, update_graph):
        self.update_graph = update_graph
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
        
        self.scope_sector = Select(
            title='Group', 
            value='Consumer Discretionary', 
            options=sectors, 
            visible=False
        )
        self.scope_sector.on_change('value', self.general_change_handler)
        
        self.scope_ticker = AutocompleteInput(
            title='Group', 
            placeholder='Input name of the asset...', 
            completions=tickers, 
            search_strategy='includes', 
            visible=False
        )
        self.scope_ticker.on_change('value', self.general_change_handler)

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
        self.size_checkbox.on_change('active', self.size_checkbox_change_handler)

        self.size_mean = Div(
            text='<p>Sample mean from the past: </p>'
        )

        self.size_mean_range = NumericInput(
            value=30,
            low=1,
            width=50,
            disabled=True
        )

        self.size_mean_unit = Select(
            value='days',
            options=['days','months','years'],
            disabled=True
        )

        self.size_mean_help = HelpButton(
            tooltip=Tooltip(
                content=HTML(
                """
                This is a tooltip with additional information.<br />
                It can use <b>HTML tags</b> like <a href="https://bokeh.org">links</a>!
                """
                ),
                position="right"
            )
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
        self.color_checkbox.on_change('active', self.color_checkbox_change_handler)

        self.color_mean = Div(
            text='<p>Sample mean from the past: </p>'
        )

        self.color_mean_range = NumericInput(
            value=30,
            low=1,
            width=50,
            disabled=True
        )

        self.color_mean_unit = Select(
            value='days',
            options=['days','months','years'],
            disabled=True
        )
        
        self.update = Button(disabled=True, label='Show Results')
        self.update.on_click(self.update_handler)

        self.controls = column(
            self.title,
            row(self.scope, self.scope_sector, self.scope_ticker), 
            self.group_var, 
            self.size_var, 
            self.size_checkbox,
            self.size_mean,
            row(self.size_mean_range, self.size_mean_unit, self.size_mean_help),
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
                self.scope_sector.visible = False
                self.scope_ticker.visible = False
                self.group_var.value = 'Sector'
                self.group_var.options = ['Asset','Asset and score type']
                self.color_var.value = 'ESG Overall Score'
                self.color_var.options = score_types
                self.color_var.disabled = False
                self.color_checkbox.disabled = False

            case 'Sector':
                self.scope_sector.visible = True
                self.scope_ticker.visible = False
                self.group_var.value = 'Asset'
                self.group_var.options = ['Asset','Asset and score type']
                self.color_var.value = 'ESG Overall Score'
                self.color_var.options = score_types
                self.color_var.disabled = False
                self.color_checkbox.disabled = False

            case 'Asset':
                self.scope_sector.visible = False
                self.scope_ticker.visible = True
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

    def size_checkbox_change_handler(self, attr, old, new):
        self.update.disabled = False

        match len(new):
            case 0:
                self.size_mean_range.disabled = True
                self.size_mean_unit.disabled = True

            case 1:
                self.size_mean_range.disabled = False
                self.size_mean_unit.disabled = False
        pass
    
    def color_checkbox_change_handler(self, attr, old, new):
        self.update.disabled = False

        match len(new):
            case 0:
                self.color_mean_range.disabled = True
                self.color_mean_unit.disabled = True

            case 1:
                self.color_mean_range.disabled = False
                self.color_mean_unit.disabled = False
        pass

    def update_handler(self):
        # potentially susceptible to code injection when rendering title without sanitizing user input!
        self.update_graph()
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
        # TODO: input validity checks
        status = {}
        status['title'] = self.title.value
        status['scope'] = self.scope.value
        status['scope_sector'] = self.scope_sector.value
        status['scope_ticker'] = self.scope_ticker.value
        status['group_var'] = self.group_var.value
        status['size_var'] = self.size_var.value
        status['size_checkbox'] = len(self.size_checkbox.active)
        status['size_mean_range'] = self.size_mean_range.value
        status['size_mean_unit'] = self.size_mean_unit.value
        status['color_var'] = self.color_var.value
        status['color_checkbox'] = len(self.color_checkbox.active)
        status['color_mean_range'] = self.color_mean_range.value
        status['color_mean_unit'] = self.color_mean_unit.value

        # color_mean_start
        # color_mean_end


        return status
        pass
