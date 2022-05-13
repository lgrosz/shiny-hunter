from PIL import ImageColor
from threading import Thread
import click
import json
import pickle

from ClickExecute import execute
from ClickRecord import record
from detect import detect as aDetect
from pick import pick as aPick
from util import variance as aVariance

@click.group()
def cli():
    pass

@click.command(help='Pick color at screen position')
@click.option('--cformat',
              type=click.Choice(['rgb', 'hex', 'hsl', 'hwb', 'cmyk', 'ncol']),
              default='rgb',
              show_default=True,
              help='Print color as hex value')
def pick(cformat):
    click.echo('Click to pick a color')
    pos, color = aPick()

    if cformat == 'hex':
        color = '#%02x%02x%02x' % color
    elif cformat == 'hsl':
        # TODO implement
        pass
    elif cformat == 'hwb':
        # TODO implement
        pass
    elif cformat == 'cmyk':
        # TODO implement
        pass
    elif cformat == 'ncol':
        # TODO implement
        pass

    click.echo(f'position={pos}')
    click.echo(f'color={color}')

@click.command(help='Detect color at screen position')
@click.option('--pos', type=int, nargs=2, required=True, help='x y position for pixel on screen.')
@click.option('--color', type=int, nargs=3, required=True, help='r g b color for pixel.')
@click.option('--variance', type=int, default=0, help='Allowed color variance.')
def detect(pos, color, variance):
    click.echo('Waiting...')
    thread = Thread(target=aDetect, args=(pos, color, variance))
    thread.start()
    thread.join()

@click.command(help='Describe a recording')
@click.argument('file', type=click.File('rb'))
def describe(file):
    specification = pickle.load(file)
    identifiers, delay, shiny_pick = specification
    click.echo('Identifiers:')
    for i in identifiers:
        pos, color = i
        click.echo(f'\t {"#%02x%02x%02x" % color} at {pos}')
    click.echo(f'Delay to shiny pick: {delay}')
    click.echo(f'Non shiny: {"#%02x%02x%02x" % shiny_pick[1]} at {shiny_pick[0]}')

@click.command(help='Returns the variance of two colors given as hex colors')
@click.argument('c1', type=str)
@click.argument('c2', type=str)
def variance(c1, c2):
    c1AsRGB = ImageColor.getcolor(c1, "RGB")
    c2AsRGB = ImageColor.getcolor(c2, "RGB")
    click.echo(aVariance(c1AsRGB, c2AsRGB))

cli.add_command(pick)
cli.add_command(detect)
cli.add_command(record)
cli.add_command(execute)
cli.add_command(describe)
cli.add_command(variance)


if __name__ == '__main__':
    cli()

