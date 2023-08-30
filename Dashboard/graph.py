class Graph:
    """
    Intended as an abstract base class
    """

    def __init__(self, update_main):
        self.update_main = update_main

        self.init_controls()
        self.fetch_data()
        self.preprocess()
        self.render()
        pass

    def init_controls(self):
        pass

    def update(self):
        pass

    def fetch_data(self):
        pass

    def preprocess(self):
        pass

    def render(self):
        pass

    def get_controls(self):
        pass

    def get_plot(self):
        pass

    pass