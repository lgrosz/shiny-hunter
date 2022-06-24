from colorsys import rgb_to_hls
from pynput.mouse import Listener as MouseListener
import click

from api.pick import pick as aPick
from api.change_basis import Bases, change_basis

@click.command(help='Pick color at screen position')
@click.option('--colormodel',
              type=click.Choice(Bases),
              default='rgb',
              show_default=True,
              help='Print color in specific colormodel')
def pick(colormodel):
    click.echo('Click to pick a color')

    color = []

    def _selectColor(x, y, button, pressed):
        color.append(aPick(x, y))
        return False

    with MouseListener(
        on_click=_selectColor
    ) as l:
        l.join()

    if (len(color) > 0):
        click.echo(change_basis(color[0], colormodel, colormodel))
    else:
        click.echo('Failed to pick color', err=True)

