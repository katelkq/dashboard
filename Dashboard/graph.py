class Graph:
    """
    Intended as an abstract base class, but I ended up putting some code in __init__()
    To be honest, I have no idea why I wrote this class at all. But it does give a cleaner overview of the structure than the mess of the actual implementation files.
    """

    def __init__(self, update_main):
        self.update_main = update_main

        self.init_controls()
        self.fetch_data()
        self.preprocess()
        self.render()
        pass

    def init_controls(self):
        """
        """
        pass

    def update(self):
        """
        """
        pass

    def fetch_data(self):
        """
        """
        pass

    def preprocess(self):
        """
        """
        pass

    def render(self):
        """
        """
        pass

    def get_controls(self):
        """
        """
        pass

    def get_plot(self):
        """
        """
        pass

    pass