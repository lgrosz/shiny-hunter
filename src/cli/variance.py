from ast import literal_eval
from pynput.mouse import Listener as MouseListener
import click

from api.change_basis import change_basis, Bases
from api.pick import pick as aPick
from api.variance import variance as aVariance

from .util import verify_scalars


@click.command(help='Returns the variance of two rgb tuples with normalized values.')
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
@click.option('--color1', type=str, default='', help='First color to compare. If not populated one will need to be picked at runtime.')
@click.option('--color2', type=str, default='', help='Second color to compare. If not populated one will need to be picked at runtime.')
def variance(color1, color2, colormodel, scalars):
    if color1:
        color1 = literal_eval(color1)
    else:
        color1 = getColor()

    if color2:
        color2 = literal_eval(color2)
    else:
        color2 = getColor()

    if (scalars and not verify_scalars(colormodel, scalars)):
        click.echo('Invalid scalars provided', err=True)
        return

    color1 = change_basis(color1, colormodel, scalars)
    color2 = change_basis(color2, colormodel, scalars)

    click.echo(aVariance(color1, color2))

def getColor():
    click.echo('Click to pick a color')

    color = []

    def _selectColor(x, y, button, pressed):
        if (pressed):
            color.append(aPick(x, y))
            return False
        return True

    with MouseListener(
        on_click=_selectColor
    ) as l:
        l.join()

    if (len(color) > 0):
        return color[0]
    else:
        click.echo('Failed to pick color', err=True)

