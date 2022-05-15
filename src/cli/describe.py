import click

from api.descriptor import Descriptor

@click.command(help='Describe a recording')
@click.argument('file', default="-", type=click.File('r'))
def describe(file):
    d = Descriptor.from_json(file.read())
    click.echo(d)

    click.echo('Resolvers:')
    for i in d.resolvers:
        pos, color = i
        click.echo(f'\t {"#%02x%02x%02x" % tuple(color)} at {tuple(pos)}')
    click.echo(f'Shiny pick delay: {d.pick_delay}')
    click.echo(f'Expected non-shiny pick: {"#%02x%02x%02x" % tuple(d.expected_pick[1])} at {tuple(d.expected_pick[0])}')

