import click
import json

@click.command(help='Describe a recording')
@click.argument('file', default="-", type=click.File('r'))
def describe(file):
    identifiers, delay, shiny_pick = json.load(file)
    click.echo('Identifiers:')
    for i in identifiers:
        pos, color = i
        click.echo(f'\t {"#%02x%02x%02x" % tuple(color)} at {tuple(pos)}')
    click.echo(f'Delay to shiny pick: {delay}')
    click.echo(f'Non shiny: {"#%02x%02x%02x" % tuple(shiny_pick[1])} at {tuple(shiny_pick[0])}')

