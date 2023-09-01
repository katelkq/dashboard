from bokeh.layouts import column, row
from bokeh.models import Tooltip
from bokeh.models.dom import HTML
from bokeh.models.widgets import *
from datetime import datetime, timedelta

from params import *

class HeatmapControls:
    """
    Contain control widgets for the heatmap and implement control logic.

    """

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
            title='Sector', 
            value=sectors[0], 
            options=sectors, 
            visible=False
        )
        self.scope_sector.on_change('value', self.general_change_handler)
        
        self.scope_asset = AutocompleteInput(
            title='Asset', 
            placeholder='Input name of the asset...', 
            completions=assets, 
            search_strategy='starts_with', 
            visible=False
        )
        self.scope_asset.on_change('value', self.general_change_handler)

        self.group_var = Select(
            title='Group Variable', 
            value='Asset', 
            options=['Asset']
        )
        self.group_var.on_change('value', self.group_var_handler)

        self.size_var = Select(
            title='Size Variable', 
            value='Buzz', 
            options=core
        )
        self.size_var.on_change('value', self.general_change_handler)

        self.size_checkbox = CheckboxGroup(
            labels=['Assign size by number of deviations from mean'],
            active=[],
            visible=False
        )
        self.size_checkbox.on_change('active', self.size_checkbox_change_handler)

        self.size_mean = Div(
            text='<p>Sample mean from the past: </p>',
            visible=False
        )

        self.size_mean_range = NumericInput(
            value=30,
            low=1,
            width=50,
            visible=False,
            disabled=True
        )
        self.size_mean_range.on_change('value', self.general_change_handler)

        self.size_mean_unit = Select(
            value='days',
            options=['days','weeks','months','years'],
            visible=False,
            disabled=True
        )
        self.size_mean_unit.on_change('value', self.general_change_handler)

        # TODO: add help message
        self.size_mean_help = HelpButton(
            tooltip=Tooltip(
                content=HTML(
                """
                This is a tooltip with additional information.<br />
                It can use <b>HTML tags</b> like <a href="https://bokeh.org">links</a>!
                """
                ),
                position="right"
            ),
            visible=False
        )

        self.color_var = Select(
            title='Color Variable', 
            value='ESG Overall Score', 
            options=core
        )
        self.color_var.on_change('value', self.general_change_handler)

        self.color_checkbox = CheckboxGroup(
            labels=['Assign color by number of deviations from mean'],
            active=[],
            visible=False
        )
        self.color_checkbox.on_change('active', self.color_checkbox_change_handler)

        self.color_mean = Div(
            text='<p>Sample mean from the past: </p>',
            visible=False
        )

        self.color_mean_range = NumericInput(
            value=30,
            low=1,
            width=50,
            visible=False,
            disabled=True
        )
        self.color_mean_range.on_change('value', self.general_change_handler)

        self.color_mean_unit = Select(
            value='days',
            options=['days', 'weeks', 'months','years'],
            visible=False,
            disabled=True
        )
        self.color_mean_unit.on_change('value', self.general_change_handler)
        
        # TODO: add help message
        self.color_mean_help = HelpButton(
            tooltip=Tooltip(
                content=HTML(
                """
                This is a tooltip with additional information.<br />
                It can use <b>HTML tags</b> like <a href="https://bokeh.org">links</a>!
                """
                ),
                position="right"
            ),
            visible=False
        )

        self.update = Button(disabled=True, label='Show Results')
        self.update.on_click(self.update_handler)

        self.controls = column(
            self.title,
            row(self.scope, self.scope_sector, self.scope_asset), 
            self.group_var, 
            self.size_var, 
            self.size_checkbox,
            self.size_mean,
            row(self.size_mean_range, self.size_mean_unit, self.size_mean_help),
            self.color_var, 
            self.color_checkbox,
            self.color_mean,
            row(self.color_mean_range, self.color_mean_unit, self.color_mean_help),
            self.update
        )
        pass

    def general_change_handler(self, attr, old, new):
        """
        Make update button clickable after changes to control status.
        
        """

        self.update.disabled = False
        pass

    def scope_handler(self, attr, old, new):
        """
        Propagate changes to other widgets after the scope of the graph has been changed.
        
        """

        self.update.disabled = False

        match new:
            # when we want to plot the scores for a single asset
            case 'Asset':
                self.scope_sector.visible = False
                self.scope_asset.visible = True

                self.group_var.value = 'Score type'
                self.group_var.options = ['Score type']

                self.size_var.visible = False

                self.size_checkbox.active = []
                self.size_checkbox.visible = True
                self.size_mean.visible = True
                self.size_mean_range.visible = True
                self.size_mean_unit.visible = True
                self.size_mean_help.visible = True

                self.color_var.visible = False

                self.color_checkbox.active = []
                self.color_checkbox.visible = True
                self.color_mean.visible = True
                self.color_mean_range.visible = True
                self.color_mean_unit.visible = True
                self.color_mean_help.visible = True

            case _:
                self.scope_sector.visible = new == 'Sector'
                self.scope_asset.visible = False

                self.group_var.value = 'Asset'
                self.group_var.options = ['Asset']

                self.size_var.value = 'Buzz'
                self.size_var.options = core
                self.size_var.visible = True
                
                self.size_checkbox.active = []
                self.size_checkbox.visible = False
                self.size_mean.visible = False
                self.size_mean_range.visible = False
                self.size_mean_unit.visible = False
                self.size_mean_help.visible = False

                self.color_var.value = 'ESG Overall Score'
                self.color_var.options = core
                self.color_var.visible = True

                self.color_checkbox.active = []
                self.color_checkbox.visible = False
                self.color_mean.visible = False
                self.color_mean_range.visible = False
                self.color_mean_unit.visible = False
                self.color_mean_help.visible = False
        pass

    def group_var_handler(self, attr, old, new):
        """
        Currently not in use.
        
        Can potentially be revived, if we want to allow each block to contain information on one specific score from one specific asset, within a limited universe e.g. a single sector. This would allow the user to see the bigger picture from a bigger universe.

        """

        self.update.disabled = False

        match new:
            case 'Asset':
                self.color_var.value = 'ESG Overall Score'
                self.color_var.options = core
                self.color_var.disabled = False
                self.color_checkbox.disabled = False

            # deprecated branch. maybe it will be revived some day?
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
        self.status['scope'] = self.scope.value

        # map asset name to assetCode, if needed
        if self.status['scope'] == 'Asset':
            self.status['asset_code'] = equcor_assets.loc[equcor_assets['name'] == self.scope_asset.value, 'assetCode'].to_string(index=False)
        
        self.status['scope_sector'] = self.scope_sector.value
        self.status['scope_ticker'] = self.scope_asset.value
        self.status['group_var'] = self.group_var.value

        # disambiguates if the score belongs to Core or Advanced; the else branch is currently not in use (as only Core is allowed at the moment)
        if self.size_var.value in equcor_datacols['name'].values:
            self.status['size_var'] = equcor_datacols.loc[equcor_datacols['name'] == self.size_var.value, 'code'].to_string(index=False)
            self.status['size_var_core'] = True
        else:
            self.status['size_var'] = equesg_datacols.loc[equesg_datacols['name'] == self.size_var.value, 'code'].to_string(index=False)
            self.status['size_var_core'] = False

        self.status['size_checkbox'] = len(self.size_checkbox.active) != 0

        # if checkbox is ticked, extend time range of query as appropriate
        if self.status['size_checkbox']:
            match self.size_mean_unit.value:
                case 'days':
                    days = int(self.size_mean_range.value)
                case 'weeks':
                    days = 7 * int(self.size_mean_range.value)
                case 'months':
                    days = 30 * int(self.size_mean_range.value)
                case 'years':
                    days = 365 * int(self.size_mean_range.value)

            self.status['size_mean_start'] = datetime.date(datetime.now()) - timedelta(days=days)
            self.status['size_mean_end'] = datetime.date(datetime.now())
            self.status['size_mean_interval'] = days
        else:
            self.status['size_mean_start'] = datetime.date(datetime.now()) - timedelta(days=1)
            self.status['size_mean_end'] = datetime.date(datetime.now())

        # similarly, else branch not in use
        if self.color_var.value in equcor_datacols['name'].values:
            self.status['color_var'] = equcor_datacols.loc[equcor_datacols['name'] == self.color_var.value, 'code'].to_string(index=False)
            self.status['color_var_core'] = True
        else:
            self.status['color_var'] = equesg_datacols.loc[equesg_datacols['name'] == self.color_var.value, 'code'].to_string(index=False)
            self.status['color_var_core'] = False

        self.status['color_checkbox'] = len(self.color_checkbox.active) != 0

        # if checkbox is ticked, extend time range of query as appropriate
        if self.status['color_checkbox']:
            match self.color_mean_unit.value:
                case 'days':
                    days = int(self.color_mean_range.value)
                case 'weeks':
                    days = 7 * int(self.color_mean_range.value)
                case 'months':
                    days = 30 * int(self.color_mean_range.value)
                case 'years':
                    days = 365 * int(self.color_mean_range.value)

            self.status['color_mean_start'] = datetime.date(datetime.now()) - timedelta(days=days)
            self.status['color_mean_end'] = datetime.date(datetime.now())
            self.status['color_mean_interval'] = days
        else:
            self.status['color_mean_start'] = datetime.date(datetime.now()) - timedelta(days=1)
            self.status['color_mean_end'] = datetime.date(datetime.now())

        return self.status
        pass
