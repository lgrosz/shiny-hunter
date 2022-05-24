import click
import json
import matplotlib.pyplot as plt

from api.change_basis import change_basis


@click.command(help='A 2D graph with hue on the y axis and encounters on x axis')
@click.argument('logs', type=click.File('r'), nargs=-1)
def hue_v_encounter(logs):
    if (len(logs) < 1):
        click.echo('No files specified', err=True)
        return

    logs = map(lambda log: json.load(log), logs)

    # TODO mark each encounter with the file it was gotten from
    # TODO mark each encounter with a hash of the descriptor used

    fig, ax = plt.subplots()
    for log in logs:
        encounters = log['encounters']
        hues = list(map(lambda e: change_basis(e['pick'], 'hsl', 'h')[0], encounters))
        colors = list(map(lambda e: e['pick'], encounters))
        encounters = range(len(encounters))
        ax.scatter(encounters, hues, c=colors)

    ax.set_xlabel('Encounters')
    ax.set_ylabel('Hue')
    ax.set_title('Hue by Encounter')

    plt.show()

