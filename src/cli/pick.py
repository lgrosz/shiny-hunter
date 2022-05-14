import click

from api.pick import pick as aPick

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

