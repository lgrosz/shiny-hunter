from pynput.keyboard import Listener as KBListener, Key
from pynput.mouse import Listener as MouseListener, Button
from threading import Thread
from time import perf_counter
import click
import gi

from api.descriptor import Descriptor

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from api.detect import detect
from api.pick import pick


class IdentifierPicker(Thread):
    '''
    Populates a given array with picks
    '''
    def __init__(self, identifiers):
        Thread.__init__(self)
        self.identifiers = identifiers
        self.finished = False

    def run(self):
        while not self.finished:
            with MouseListener(
                on_click=self._pick
            ) as l:
                l.join()

    def _pick(self, x, y, button, pressed):
        if (pressed):
            pixbuf = Gdk.pixbuf_get_from_window(Gdk.get_default_root_window(), x, y, 1, 1)
            self.identifiers.append(((x, y), tuple(pixbuf.get_pixels()),))
            click.echo(f'Picked {"#%02x%02x%02x" % self.identifiers[-1][1]}', err=True)
            if (button == Button.left):
                self.finished = True
        return False


class IdentifierEnder(Thread):
    '''
    Notifies when the picking process should be ended
    '''
    def _on_press(self, key):
        if (key == Key.enter):
            return False
        else:
            return True

    def __init__(self, identifiers):
        Thread.__init__(self)
        self.identifiers = identifiers

    def run(self):
        while True:
            if (len(self.identifiers) > 0):
                click.echo('Press `return` to finish')
                with KBListener(
                    on_press=self._on_press
                ) as l:
                    l.join()
                    break;


@click.option('--variance', type=int, default=0, help='Allowed color variance. Used when replaying to get perform shiny pick. NOT IMPLEMENTED.')
@click.option('--file', type=click.File('w'), default='-', help='Path to file to save descriptor in.')
@click.command(help='Records a shiny detector package. Saves to file.')
def record(variance, file):
    click.echo('Pick at least one identifer. Use right click to select more, left click to select the last one.', err=True)

    identifiers = []
    picker = IdentifierPicker(identifiers)
    picker.start()
    picker.join()

    click.echo('Attempting to resolve identity...', err=True)
    for i in identifiers:
        pos, color = i
        detect(pos, color)
    start = perf_counter()
    click.echo('Identifiers resolved. Click the shiny color when available.', err=True)

    expected_color = []
    expected_pos = []
    def _selectColor(x, y, button, pressed):
        expected_pos.append((x, y))
        expected_color.append(pick(x, y))
        return False

    with MouseListener(
        on_click=_selectColor
    ) as l:
        l.join()

    delay = perf_counter() - start

    descriptor = Descriptor(identifiers, delay, (expected_pos[0], expected_color[0]))
    file.write(descriptor.to_json())

