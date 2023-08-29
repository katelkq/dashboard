from bokeh.plotting import figure

class SamplePlot:
    """
    Just a simple plot inside a class wrapper.
    For testing things out.
    """

    def __init__(self):
        # prepare some data
        x = [1, 2, 3, 4, 5]
        y1 = [6, 7, 2, 4, 5]
        y2 = [2, 3, 4, 5, 6]
        y3 = [4, 5, 5, 7, 2]

        # create a new plot with a title and axis labels
        self.plot = figure(
            title="Multiple line example", 
            x_axis_label="x", 
            y_axis_label="y",
        )

        # add multiple renderers
        self.plot.line(x, y1, legend_label="Temp.", line_color="blue", line_width=2)
        self.plot.line(x, y2, legend_label="Rate", line_color="red", line_width=2)
        self.plot.line(x, y3, legend_label="Objects", line_color="green", line_width=2)
    pass
