import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from time import perf_counter

# 5100, 905

start = perf_counter()
geometry = Gdk.Display.get_default().get_monitor_at_point(5100, 905).get_geometry()
end = perf_counter()
print(f'Pixel capture took {end-start}s')
#pixbuf = Gdk.pixbuf_get_from_window(Gdk.get_default_root_window(), x, y, 1, 1)

