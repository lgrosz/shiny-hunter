from ast import literal_eval
from pynput.mouse import Listener as MouseListener
from statistics import mean
import click
import json

from api.change_basis import change_basis, Bases
from api.pick import pick as aPick
from api.variance import variance as aVariance

from .util import verify_scalars


# TODO This can possibly optimize colormodel and scalars as well
@click.command(help='Takes many rgb tuples and calculates their maximum variance')
@click.option('--colormodel',
              type=click.Choice(Bases),
              default='rgb',
              show_default=True,
              help='The colormodel to convert to')
@click.option('--scalar', 'scalars',
              type=str,
              default=[],
              multiple=True,
              help='The scarals of the colormodel to reduce the span to')
@click.argument('logs', type=click.File('r'), required=True, nargs=-1)
def optimize_variance(colormodel, scalars, logs):
    if (scalars and not verify_scalars(colormodel, scalars)):
        click.echo('Invalid scalars provided', err=True)
        return

    logs = list(map(lambda log: json.load(log), logs))

    # Parse picked colors from all encounters
    colors = []
    for log in logs:
        encounters = log['encounters']
        for encounter in encounters:
            r, g, b = encounter['pick']
            colors.append((r, g, b))

    distances = []
    for i, color1 in enumerate(colors):
        distances.append([])
        for color2 in colors:
            color1_new_basis = change_basis(color1, colormodel, scalars)
            color2_new_basis = change_basis(color2, colormodel, scalars)
            distances[i].append(aVariance(color1_new_basis, color2_new_basis))

    average_distance = list(map(lambda col: mean(col), distances))
    min_distance = min(average_distance)
    color_index = average_distance.index(min_distance)

    central_color = colors[color_index]
    max_variance = max(distances[color_index])
    
    click.echo({
        'color': central_color,
        'max_variance': max_variance
    })


