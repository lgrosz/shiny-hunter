import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from pynput.mouse import Listener as MouseListener

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

