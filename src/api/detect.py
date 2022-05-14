import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from api.variance import variance

# TODO Add param "transform", which will transform the pixbuf's pixels to
# something compatible with typeof color
def detect(pos, color, _variance=0):
    '''
    Detects the colored pixel at the given location. A tolerance can be
    provided as well as a timeout. This function is blocking.

    pos := (x, y) position of the screen
    color: = (r, g, b) color of the pixel
    _variance := maximum allowed color variance where variance is the square of
                 the Euclidean distance between two colors.

    '''
    while True:
        pixbuf = Gdk.pixbuf_get_from_window(Gdk.get_default_root_window(), pos[0], pos[1], 1, 1)
        c = tuple(pixbuf.get_pixels())
        if (variance(c, color) <= _variance):
            break

