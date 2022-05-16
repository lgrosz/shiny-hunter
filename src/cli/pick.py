import click
from pynput.mouse import Listener as MouseListener

from api.pick import pick as aPick

@click.command(help='Pick color at screen position')
@click.option('--cformat',
              type=click.Choice(['rgb', 'hex', 'hsl', 'hwb', 'cmyk', 'ncol']),
              default='rgb',
              show_default=True,
              help='Print color as hex value')
def pick(cformat):
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
        click.echo(color[0])
    else:
        click.echo('Failed to pick color', err=True)

