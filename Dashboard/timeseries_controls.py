from bokeh.layouts import column, row
from bokeh.models import Tooltip
from bokeh.models.dom import HTML
from bokeh.models.widgets import *
from datetime import datetime, timedelta

from params import *

class TimeSeriesControls:
    """
    Contain control widgets for the time series and implement control logic.

    """

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

        self.radio = RadioGroup(
            labels=['Graph data points with no transformation', 'Graph data points as change in value'],
            active=0
        )
        self.radio.on_change('active', self.radio_change_handler)

        self.change = Div(
            text='<p>Measure change since the past: </p>'
        )

        self.change_range = NumericInput(
            value=7,
            low=1,
            width=50,
            disabled=True
        )
        self.change_range.on_change('value', self.general_change_handler)

        self.change_unit = Select(
            value='days',
            options=['days','weeks','months','years'],
            disabled=True
        )
        self.change_unit.on_change('value', self.general_change_handler)

        # TODO: add help message
        self.change_help = HelpButton(
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

        self.mean_checkbox = CheckboxGroup(
            labels=['Highlight data by minimum number of deviations from mean'],
            active=[]
        )
        self.mean_checkbox.on_change('active', self.mean_checkbox_change_handler)

        self.mean = Div(
            text='<p>Sample mean from the past: </p>'
        )

        self.mean_range = NumericInput(
            value=90,
            low=1,
            width=50,
            disabled=True
        )
        self.mean_range.on_change('value', self.general_change_handler)

        self.mean_unit = Select(
            value='days',
            options=['days','weeks','months','years'],
            disabled=True
        )
        self.mean_unit.on_change('value', self.general_change_handler)

        self.mean_help = HelpButton(
            tooltip=Tooltip(
                content=HTML(
                """
                <b>Change in value</b> is calculated as the difference between each value and its corresponding past value from the specified point in time.<br />
                <b>Mean</b> is calculated as the moving linear average of the value over the specified time period.<br />
                The values that are more than the specified distance of standard deviations away from its corresponding mean are then highlighted.
                """
                ),
                position="right"
            )
        )

        self.std = Spinner(
            title='Number of standard deviations from mean: ',
            value=1.5,
            low=0,
            step=0.25,
            width=100,
            disabled=True
        )
        self.std.on_change('value', self.general_change_handler)
        
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
            self.radio,
            self.change,
            row(self.change_range, self.change_unit, self.change_help),
            self.mean_checkbox,
            self.mean,
            row(self.mean_range, self.mean_unit, self.mean_help),
            row(self.std),
            row(self.start_date, self.end_date),
            self.update
        )
        pass

    def general_change_handler(self, attr, old, new):
        """
        Make update button clickable after changes to control status.
        
        """

        self.update.disabled = False
        pass

    def radio_change_handler(self, attr, old, new):
        self.update.disabled = False

        match new:
            case 0:
                self.change_range.disabled = True
                self.change_unit.disabled = True

            case 1:
                self.change_range.disabled = False
                self.change_unit.disabled = False

        pass

    def mean_checkbox_change_handler(self, attr, old, new):
        self.update.disabled = False

        match len(new):
            case 0:
                self.mean_range.disabled = True
                self.mean_unit.disabled = True
                self.std.disabled = True

            case 1:
                self.mean_range.disabled = False
                self.mean_unit.disabled = False
                self.std.disabled = False
        pass

    def update_handler(self):
        """
        Disable the update button and initiate the update of graph.
        
        """

        self.update.disabled = True
        self.update_graph()
        pass

    def get_controls(self):
        return self.controls
        pass

    def get_status(self):
        """
        Return a dictionary of the current control status.
        
        """

        # TODO: input validity checks and error messages
        self.status['title'] = self.title.value

        # map asset name to assetCode
        self.status['asset'] = equcor_assets.loc[equcor_assets['name'] == self.asset.value, 'assetCode'].to_string(index=False)

        # disambiguates if the score belongs to Core or Advanced; the else branch is currently not in use (as only Core is allowed at the moment)
        if self.var.value in equcor_datacols['name'].values:
            self.status['var'] = equcor_datacols.loc[equcor_datacols['name'] == self.var.value, 'code'].to_string(index=False)
            self.status['var_core'] = True
        else:
            self.status['var'] = equesg_datacols.loc[equesg_datacols['name'] == self.var.value, 'code'].to_string(index=False)
            self.status['var_core'] = False

        self.status['radio'] = self.radio.active
        if self.status['radio'] != 0:
            match self.change_unit.value:
                case 'days':
                    self.status['change_days'] = int(self.change_range.value)
                case 'months':
                    self.status['change_days'] = 30 * int(self.change_range.value)
                case 'years':
                    self.status['change_days'] = 365 * int(self.change_range.value)

        self.status['mean_checkbox'] = len(self.mean_checkbox.active) != 0

        if self.status['mean_checkbox']:
            match self.mean_unit.value:
                case 'days':
                    self.status['mean_days'] = int(self.mean_range.value)
                case 'months':
                    self.status['mean_days'] = 30 * int(self.mean_range.value)
                case 'years':
                    self.status['mean_days'] = 365 * int(self.mean_range.value)

        self.status['std'] = float(self.std.value)

        # TODO: timeframe has not been extended to accomodate extra data need when backward mean is required. Too much complications
        self.status['start_date'] = self.start_date.value
        self.status['end_date'] = self.end_date.value

        return self.status
        pass
