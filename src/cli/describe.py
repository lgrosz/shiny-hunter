import click
import pickle

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

