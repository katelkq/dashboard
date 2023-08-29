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

class Controls:

    def __init__(self, index, update):
        self.index = index
        self.update_graph = update
        self.changed = False
        self.status = {}

        # initializing graph control widgets
        self.type_of_graph = Select(
            title='Type of Graph', 
            value='Heatmap', 
            options=['Heatmap', 'Timeseries']
        )
        self.type_of_graph.on_change('value', self.general_change_handler)

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
        
        universe = row(self.scope, self.group_sector, self.group_ticker)

        self.group_var = Select(
            title='Group Variable', 
            value='Asset', 
            options=['Sector', 'Asset', 'Asset and score type'])
        self.group_var.on_change('value', self.group_var_handler)

        self.color_var = Select(
            title='Color Variable', 
            value='ESG Overall Score', 
            options=score_types)
        
        self.size_var = Select(
            title='Size Variable', 
            value='Buzz', 
            options=['Buzz', 'Change in Buzz'])

        # TODO: impose temporal logic

        self.update_freqeuncy = Select(
            title='Update Frequency',
            value='Daily',
            options=['1 minute', '1 hour', 'Daily']
        )

        self.start = DatePicker(
            title='Start',
            value=datetime.date(datetime.now()) - timedelta(days=1),
            min_date="2019-08-01T09:00:00",
            max_date=datetime.date(datetime.now())
        )

        self.end = DatePicker(
            title='End',
            value=datetime.date(datetime.now()),
            min_date="2019-08-01T09:00:00",
            max_date=datetime.date(datetime.now())
        )

        self.alternative = Div(
            text='<p>Alternatively, select a point in time and specify a relative range: </p>'
        )

        self.date = DatePicker(
            value=datetime.date(datetime.now()),
            max_date=datetime.date(datetime.now())
        )

        self.date_and_time = DatetimePicker(
            value=datetime.now(),
            max_date=datetime.now(),
            visible=False
        )

        self.shift = NumericInput(
            value=30,
            low=1,
            width=50
        )

        self.unit = Select(
            value='days',
            options=['minutes','hours','days','months','years']
        )

        self.shift_direction = Select(
            value='before',
            options=['after','before']
        )

        self.apply = Button(disabled=True, label='Apply')
        self.apply.on_click(self.apply_handler)

        self.controls = column(
            row(self.type_of_graph, self.title),
            universe, 
            row(self.group_var, self.color_var), 
            row(self.update_freqeuncy), 
            row(self.start, self.end), 
            self.alternative, 
            row(self.date, self.date_and_time, self.shift, self.unit, self.shift_direction),
            self.apply
        )
        pass

    def general_change_handler(self, attr, old, new):
        self.apply.disabled = False
        pass

    def scope_handler(self, attr, old, new):
        self.apply.disabled = False

        match new:
            case 'All':
                self.group_sector.visible = False
                self.group_ticker.visible = False
                self.group_var.value = 'Sector'
                self.group_var.options = ['Sector','Asset','Asset and score type']
                self.color_var.value = 'ESG Score'
                self.color_var.options = score_types
                self.color_var.disabled = False

            case 'Sector':
                self.group_sector.visible = True
                self.group_ticker.visible = False
                self.group_var.value = 'Asset'
                self.group_var.options = ['Asset','Asset and score type']
                self.color_var.value = 'ESG Score'
                self.color_var.options = score_types
                self.color_var.disabled = False

            case 'Ticker':
                self.group_sector.visible = False
                self.group_ticker.visible = True
                self.group_var.value = 'Score type'
                self.group_var.options = ['Score type']
                self.color_var.value = '-'
                self.color_var.options = ['-']
                self.color_var.disabled = True
        pass

    def group_var_handler(self, attr, old, new):
        self.apply.disabled = False

        match new:
            case 'Sector':
                self.color_var.value = 'ESG Score'
                self.color_var.options = score_types
                self.color_var.disabled = False

            case 'Ticker':
                self.color_var.value = 'ESG Score'
                self.color_var.options = score_types
                self.color_var.disabled = False

            case 'Ticker and score type':
                self.color_var.value = '-'
                self.color_var.options = ['-']
                self.color_var.disabled = True
        pass


    def apply_handler(self):
        # potentially susceptible to code injection
        self.update_graph(self.get_status())
        self.apply.disabled = True
        pass

    def get_controls(self):
        return self.controls
        pass

    def get_status(self):
        status = {}
        status['type_of_graph'] = self.type_of_graph.value
        status['title'] = self.title.value
        status['scope'] = self.scope.value
        status['group_sector'] = self.group_sector.value
        status['group_ticker'] = self.group_ticker.value
        status['group_var'] = self.group_var.value
        status['color_var'] = self.color_var.value
        status['update_freqeuncy'] = self.update_freqeuncy.value
        status['start'] = self.start.value
        status['end'] = self.end.value
        return status
        pass
