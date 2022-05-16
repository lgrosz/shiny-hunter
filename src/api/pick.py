import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
import logging
from sys import stderr
from time import perf_counter


logging.basicConfig(filename='api-pick.log', level=logging.INFO)

def pick(x, y) -> tuple[int, int, int]:
    '''
    On click, return ((x,y), (r, g, b)) where (r, g, b) is
    the color of the pixel at position (x, y) on the screen.
    This function is blocking.
    '''
    start = perf_counter()
    pixbuf = Gdk.pixbuf_get_from_window(Gdk.get_default_root_window(), x, y, 1, 1)
    end = perf_counter()
    logging.info(f'Pixel capture took {end-start}')
    return _normalize(tuple(pixbuf.get_pixels()), 2**pixbuf.get_bits_per_sample()-1)

def _normalize(l, m):
    '''
    Return copy of l normalized to m
    '''
    return tuple([x/m for x in l])

