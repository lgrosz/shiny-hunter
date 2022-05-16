from time import sleep
import click
import gi

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from api.descriptor import Descriptor
from api.detect import detect
from api.variance import variance as aVariance


@click.option('--identifier_variance', type=int, default=1000, show_default=True, help='Allowed color variance. NOT IMPLEMENTED.')
@click.option('--shiny_variance', type=int, default=1000, show_default=True, help='Allowed color variance. NOT IMPLEMENTED.')
@click.option('--debounce', type=int, default=0, help='Second to debounce the identifier resolver after a (non)shiny pick')
@click.argument('file', default='-', type=click.File('r'))
@click.command(help='Records a shiny detector package. Saves to file.')
def execute(identifier_variance, shiny_variance, debounce, file):
    descriptor = Descriptor.from_json(file.read())

    resets = 0
    found = False

    while not found:
        click.echo('Resolving identifers...')
        for i in descriptor.resolvers:
            pos, color = i
            detect(pos, color, _variance=identifier_variance)

        click.echo('Delaying for shiny pick...')
        sleep(descriptor.pick_delay)

        shiny_loc, shiny_color = descriptor.expected_pick
        pixbuf = Gdk.pixbuf_get_from_window(Gdk.get_default_root_window(), shiny_loc[0], shiny_loc[1], 1, 1)
        picked_color = tuple(pixbuf.get_pixels())

        click.echo(f'Picked {"#%02x%02x%02x" % picked_color}')
        if (aVariance(picked_color, shiny_color) >= shiny_variance):
            found = True
        else:
            click.echo('Not shiny')
            resets += 1
            sleep(debounce)


    click.echo(f'Found shiny in {resets} resets.')

