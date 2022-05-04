from time import sleep
import gi
from threading import Thread

from util import variance as aVariance

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk


def detect(pos, color, variance=0):
    '''
    Detects the colored pixel at the given location. A
    tolerance can be provided as well as a timeout. This function is blocking.

    pos := (x, y) position of the screen
    color: = (r, g, b) color of the pixel
    variance := maximum allowed color variance where variance is the square of
                the Euclidean distance between two colors.
    '''
    while True:
        pixbuf = Gdk.pixbuf_get_from_window(Gdk.get_default_root_window(), pos[0], pos[1], 1, 1)
        c = tuple(pixbuf.get_pixels())
        if (aVariance(c, color) <= variance):
            break

