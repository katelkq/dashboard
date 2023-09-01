class Graph:
    """
    (Mostly) an abstract base class for the graphs on display.

    """

    def __init__(self, update_main):
        """
        :param update_main: Method to refresh the plot being displayed in the main interface as appropriate.

        """
        self.update_main = update_main

        self.init_controls()
        self.fetch_data()
        self.preprocess()
        self.render()
        pass

    def init_controls(self):
        """
        Initialize the control widgets for the graph and retrieve a snapshot of the default control status.

        """
        pass

    def update(self):
        """
        Retrieve the current control status, update the graph accordingly, then propagate the change to the main interface.

        """
        pass

    def fetch_data(self):
        """
        Retrieve relevant data from Refinitiv based on the current control status.

        """
        pass

    def preprocess(self):
        """
        Perform calculations based on the raw data from Refinitiv to derive additional data as required and facilitate graphing.

        """
        pass

    def render(self):
        """
        Render the interactive plot using Bokeh.

        """
        pass

    def get_controls(self):
        """
        :return: The control widgets as a single DOM element.

        """
        pass

    def get_plot(self):
        """
        :return: The plot as a single DOM element.

        """
        pass

    pass