from ast import literal_eval
from pynput.mouse import Listener as MouseListener
import click

from api.change_basis import change_basis
from api.pick import pick as aPick
from api.variance import variance as aVariance

from .util import verify_scalars


@click.command(help='Converts a given rgb tuple to the provided colormodel reduced to the given scalars')
@click.option('--colormodel',
              type=click.Choice(['rgb', 'hls']),
              default='rgb',
              show_default=True,
              help='The colormodel to convert to')
@click.option('--scalar', 'scalars',
              type=str,
              default=[],
              multiple=True,
              help='The scarals of the colormodel to reduce the span to')
@click.argument('color', type=str)
def convert(colormodel, scalars, color):
    color = literal_eval(color)

    if (scalars and not verify_scalars(colormodel, scalars)):
        click.echo('Invalid scalars provided', err=True)
        return

    color = change_basis(color, colormodel, scalars)

    click.echo(color)

