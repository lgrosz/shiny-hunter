from os import environ
from time import sleep, strftime, perf_counter
from pynput.mouse import Listener as MouseListener
import click
import json

from api.descriptor import Descriptor
from api.detect import detect
from api.pick import pick
from api.variance import variance as aVariance


# TODO Apparently dest comes second in this case.. what?
@click.argument('dest', default='-', type=click.File('w'))
@click.argument('src', default='-', type=click.File('r'))
@click.command(help='Picking the final shiny color can be a bit stressful after spending a lot of time setting up resolvers... This is meant to fix a bad final shiny pick.')
def fix_expected(src, dest):
    descriptor = Descriptor.from_json(src.read())

    click.echo('Resolving identifers...', err=True)
    for i in descriptor.resolvers:
        pos, color = i
        c = detect(pos, color, descriptor.colormodel, descriptor.scalars, descriptor.variance)

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

    new_descriptor = Descriptor(descriptor.resolvers, delay, (expected_pos[0],
                                                              expected_color[0]),
                                descriptor.colormodel, descriptor.scalars,
                                descriptor.variance)

    dest.write(new_descriptor.to_json());

