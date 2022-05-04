from detect import detect
from pick import pick
from time import sleep
import click
import gi
import pickle

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from util import variance as aVariance


@click.option('--identifier_variance', type=int, default=1000, show_default=True, help='Allowed color variance. NOT IMPLEMENTED.')
@click.option('--shiny_variance', type=int, default=1000, show_default=True, help='Allowed color variance. NOT IMPLEMENTED.')
@click.option('--debounce', type=int, default=0, help='Second to debounce the identifier resolver after a (non)shiny pick')
@click.argument('file', type=click.File('rb'))
@click.command(help='Records a shiny detector package. Saves to file.')
def execute(identifier_variance, shiny_variance, debounce, file):
    specification = pickle.load(file)

    identifiers, delay, shiny_pick = specification
    resets = 0
    found = False

    while not found:
        click.echo('Resolving identifers...')
        for i in identifiers:
            pos, color = i
            detect(pos, color, variance=identifier_variance)

        click.echo('Delaying for shiny pick...')
        sleep(delay)

        pixbuf = Gdk.pixbuf_get_from_window(Gdk.get_default_root_window(), shiny_pick[0][0], shiny_pick[0][1], 1, 1)
        picked_color = tuple(pixbuf.get_pixels())

        click.echo(f'Picked {"#%02x%02x%02x" % picked_color}')
        if (aVariance(picked_color, shiny_pick[1]) >= shiny_variance):
            found = True
        else:
            click.echo('Not shiny')
            resets += 1
            sleep(debounce)


    click.echo(f'Found shiny in {resets} resets.')

