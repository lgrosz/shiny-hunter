from copy import deepcopy
import click
import colorsys
import json
import matplotlib.pyplot as plt
import numpy as np

from api.change_basis import change_basis
from api.descriptor import Descriptor


@click.command(help='A 2D graph with hue on the y axis and encounters on x axis')
@click.argument('logs', type=click.File('r'), nargs=-1)
def hue_v_encounter(logs):
    if (len(logs) < 1):
        click.echo('No files specified', err=True)
        return

    logs = list(map(lambda log: json.load(log), logs))
    hashes = set(map(lambda log: hash(json.dumps(log['descriptor'], sort_keys=True)), logs))

    # create a subplot for each unique descriptor
    fig, ax = plt.subplots(nrows=len(hashes))

    for idx, dhash in enumerate(hashes):
        dlogs = [log for log in logs if hash(json.dumps(log['descriptor'], sort_keys=True)) == dhash]
        encounters = [encounter for log in dlogs for encounter in log['encounters']]

        hues = list(map(lambda e: change_basis(e['pick'], 'hsl', 'h')[0], encounters))
        colors = list(map(lambda e: e['pick'], encounters))
        reset_count = range(len(encounters))

        if (len(hashes) > 1):
            ax[idx].scatter(reset_count, hues, c=colors)
            ax[idx].set_xlabel('Encounters')
            ax[idx].set_ylabel('Hue')
            ax[idx].set_title(f'Descriptor {idx+1}')
        else:
            ax.scatter(reset_count, hues, c=colors)
            ax.set_xlabel('Encounters')
            ax.set_ylabel('Hue')


    plt.show()

