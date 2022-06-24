from os import environ
from time import sleep, strftime, perf_counter
from pynput.mouse import Listener as MouseListener
import click
import json

from cli.record import IdentifierPicker
from api.descriptor import Descriptor
from api.detect import detect
from api.pick import pick
from api.variance import variance as aVariance


# TODO Apparently dest comes second in this case.. what?
@click.argument('dest', default='-', type=click.File('w'))
@click.argument('src', default='-', type=click.File('r'))
@click.option('--removes', default=0, type=int, help='number of resolvers to remove from the end of the current resolver list')
@click.command(help='Adds to the resolver list. This also invalidates the expected pick as it is dependant on the final resolver.')
def fix_resolvers(src, dest, removes):
    descriptor = Descriptor.from_json(src.read())

    currentResolvers = descriptor.resolvers[0:-removes:]

    click.echo('Resolving identifers...', err=True)
    for i in currentResolvers:
        pos, color = i
        c = detect(pos, color, descriptor.colormodel, descriptor.scalars, 0.1)
    click.echo('Identifiers resolved. Choose any more you\'d like.', err=True)

    # Continue recording
    picker = IdentifierPicker(currentResolvers)
    picker.start()
    picker.join()

    click.echo('Attempting to resolve identity...', err=True)
    for i in currentResolvers:
        pos, color = i
        detect(pos, color, descriptor.colormodel, descriptor.scalars, 0.1)
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

    new_descriptor = Descriptor(currentResolvers, delay, (expected_pos[0],
                                                          expected_color[0]),
                                descriptor.colormodel, descriptor.scalars,
                                descriptor.variance)

    dest.write(new_descriptor.to_json());

