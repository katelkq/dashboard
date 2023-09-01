"""
Contains various utility functions and some related data for easy access.
"""

from datetime import datetime
import matplotlib as mpl
import numpy as np

def color_fader(c1, c2, mix=0):
    """
    Performs linear interpolation from colors c1 (at mix=0) to c2 (mix=1), both given as hex codes.

    """
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)
    pass

def color_gradient(c1, c2, steps=0):
    """
    Returns a list of hex codes from c1 to c2, with the number of specified steps in-between.

    """
    gradient = []
    delta = 1 / (steps+1)
    x = 0
    while x <= 1:
        gradient.append(color_fader(c1, c2, x))
        x += delta
    return gradient
    pass

heatmap_palette = color_gradient('#ff0000', '#008000', 100)
heatmap_palette_reversed = color_gradient('#008000', '#ff0000', 100)

def string_to_datetime(x):
    return datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z')
    pass

def datetime_to_string(x):
    return x.strftime('%Y-%m-%d')
    pass

