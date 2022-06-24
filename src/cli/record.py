from pynput.keyboard import Listener as KBListener, Key
from pynput.mouse import Listener as MouseListener, Button
from threading import Thread
from time import perf_counter
import click

from api.descriptor import Descriptor
from api.detect import detect
from api.pick import pick
from api.change_basis import Bases


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
            # Always will store the pick as rgb so we can convert it at
            # execution time. If we change it now, we risk reducing the basis.
            # For example, if we change it to h(sl), we can't change it back to
            # rgb since we've already gotten rid of the s and l parts.
            self.identifiers.append(((x, y), pick(x, y)))
            click.echo(f'Picked {self.identifiers[-1][1]}', err=True)
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


@click.option('--variance', type=float, default=0, help='Allowed color variance. Used when replaying to get perform shiny pick.')
@click.option('--colormodel',
              type=click.Choice(Bases),
              default='rgb',
              show_default=True,
              help='The colormodel at which to compute the variance. An RGB colormodel must still be passed in')
@click.option('--scalar', 'scalars',
              type=str,
              default=[],
              multiple=True,
              help='The pieces of the colormodel which to compute the variance. For example, to computer the variance of just hue, use `--colormodel hls --scalar h`')
@click.option('--file', type=click.File('w'), default='-', help='Path to file to save descriptor in.')
@click.command(help='Records a shiny detector package. Saves to file.')
def record(variance, colormodel, scalars, file):
    click.echo('Pick at least one identifer. Use right click to select more, left click to select the last one.', err=True)

    identifiers = []
    picker = IdentifierPicker(identifiers)
    picker.start()
    picker.join()

    click.echo('Attempting to resolve identity...', err=True)
    for i in identifiers:
        pos, color = i
        detect(pos, color, colormodel, scalars, 0.1)
        click.echo(f'Resolved identifier {i}', err=True)
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

    descriptor = Descriptor(identifiers, delay, (expected_pos[0],
                                                 expected_color[0]),
                            colormodel, scalars, variance)
    file.write(descriptor.to_json())

