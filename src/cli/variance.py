from PIL import ImageColor
import click

from api.variance import variance as aVariance

@click.command(help='Returns the variance of two colors given as hex colors')
@click.argument('c1', type=str)
@click.argument('c2', type=str)
def variance(c1, c2):
    c1AsRGB = ImageColor.getcolor(c1, "RGB")
    c2AsRGB = ImageColor.getcolor(c2, "RGB")
    click.echo(aVariance(c1AsRGB, c2AsRGB))

