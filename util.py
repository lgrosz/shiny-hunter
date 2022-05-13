import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from pynput.mouse import Listener as MouseListener

# TODO The params should have the same dimensions but this function should
# not depend on the actual number of them
def variance(a, b):
    '''
    Takes finds the Euclidean distance between two points
    '''
    return (b[0]-a[0])**2 + (b[1]-a[1])**2 + (b[2]-a[2])**2

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

# TODO Make this non-blocking and replace. All the other functions should not
# need to do this Gdk.pixbuf thing
def pick():
    '''
    On click, return ((x,y), (r, g, b)) where (r, g, b) is
    the color of the pixel at position (x, y) on the screen.
    This function is blocking.
    '''
    ret = []
    def _selectColor(x, y, button, pressed):
        pixbuf = Gdk.pixbuf_get_from_window(Gdk.get_default_root_window(), x, y, 1, 1)
        ret.append(((x, y), tuple(pixbuf.get_pixels()),))
        return False

    with MouseListener(
        on_click=_selectColor
    ) as l:
        l.join()
        if (len(ret) > 0):
            return ret[0]
        else:
            return None

