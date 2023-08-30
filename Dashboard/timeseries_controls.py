from bokeh.models import *
from bokeh.models.dom import HTML
from bokeh.layouts import column, row
from bokeh.plotting import *
from datetime import datetime, timedelta
from params import *

class TimeSeriesControls:

    def foo(self):
        self.update_freqeuncy = Select(
            title='Update Frequency',
            value='Daily',
            options=['1 minute', '1 hour', 'Daily']
        )
        pass

    def __init__(self, update_graph):
        self.update_graph = update_graph
        self.status = {}

        # initializing graph control widgets
        self.title = TextInput(
            title='Title',
            value='Time Series'
        )
        self.title.on_change('value', self.general_change_handler)

        self.asset = AutocompleteInput(
            title='Asset', 
            placeholder='Input name of the asset...', 
            value='Apple Inc',
            completions=assets, 
            search_strategy='includes'
        )
        self.asset.on_change('value', self.general_change_handler)

        self.var = Select(
            title='Variable', 
            value='Buzz', 
            options=core
        )
        self.var.on_change('value', self.general_change_handler)

        self.mean_checkbox = CheckboxGroup(
            labels=['Highlight data points by magnitude of deviation from mean'],
            active=[]
        )
        self.mean_checkbox.on_change('active', self.mean_checkbox_change_handler)

        self.mean = Div(
            text='<p>Sample mean from the past: </p>'
        )

        self.mean_range = NumericInput(
            value=30,
            low=1,
            width=50,
            disabled=True
        )
        self.mean_range.on_change('value', self.general_change_handler)

        self.mean_unit = Select(
            value='days',
            options=['days','months','years'],
            disabled=True
        )
        self.mean_unit.on_change('value', self.general_change_handler)

        self.mean_help = HelpButton(
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
        
        self.start_date = DatePicker(
            title='Start Date',
            value=datetime.date(datetime.now()) - timedelta(days=180),
            min_date="1998-01-01",
            max_date=datetime.date(datetime.now())
        )
        self.start_date.on_change('value', self.general_change_handler)

        self.end_date = DatePicker(
            title='End Date',
            value=datetime.date(datetime.now()),
            min_date="1998-01-01",
            max_date=datetime.date(datetime.now())
        )
        self.end_date.on_change('value', self.general_change_handler)

        self.update = Button(disabled=False, label='Show Results')
        self.update.on_click(self.update_handler)

        self.controls = column(
            self.title,
            self.asset,
            self.var, 
            self.mean_checkbox,
            self.mean,
            row(self.mean_range, self.mean_unit, self.mean_help),
            row(self.start_date, self.end_date),
            self.update
        )
        pass

    def general_change_handler(self, attr, old, new):
        self.update.disabled = False
        pass

    def mean_checkbox_change_handler(self, attr, old, new):
        self.update.disabled = False

        match len(new):
            case 0:
                self.mean_range.disabled = True
                self.mean_unit.disabled = True

            case 1:
                self.mean_range.disabled = False
                self.mean_unit.disabled = False
        pass

    def update_handler(self):
        # potentially susceptible to code injection when rendering title without sanitizing user input!
        self.update.disabled = True
        self.update_graph()
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
        self.status['title'] = self.title.value

        # map asset name to assetCode
        self.status['asset'] = equcor_assets.loc[equcor_assets['name'] == self.asset.value, 'assetCode'].to_string(index=False)

        if self.var.value in equcor_datacols['name'].values:
            self.status['var'] = equcor_datacols.loc[equcor_datacols['name'] == self.var.value, 'code'].to_string(index=False)
            self.status['var_core'] = True
        else:
            self.status['var'] = equesg_datacols.loc[equesg_datacols['name'] == self.var.value, 'code'].to_string(index=False)
            self.status['var_core'] = False

        self.status['mean_checkbox'] = len(self.mean_checkbox.active) != 0
        # if checkbox
        if self.status['mean_checkbox']:
            match self.mean_unit.value:
                case 'days':
                    self.status['mean_days'] = int(self.mean_range.value)
                case 'months':
                    self.status['mean_days'] = 30 * int(self.mean_range.value)
                case 'years':
                    self.status['mean_days'] = 365 * int(self.mean_range.value)

        self.status['start_date'] = self.start_date.value
        self.status['end_date'] = self.end_date.value

        return self.status
        pass

    pass