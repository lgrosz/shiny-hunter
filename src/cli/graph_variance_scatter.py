import click
import json
import matplotlib.pyplot as plt
import numpy as np

from api.descriptor import Descriptor
from api.change_basis import change_basis
from api.variance import variance


@click.command(help='A scatterplot showing the variance during the shiny hunt and how it relates the allowed variance.')
@click.argument('logs', type=click.File('r'), nargs=-1)
def variance_scatter(logs):
    if (len(logs) < 1):
        click.echo('No files specified', err=True)
        return

    logs = list(map(lambda log: json.load(log), logs))
    hashes = set(map(lambda log: hash(json.dumps(log['descriptor'], sort_keys=True)), logs))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for idx, dhash in enumerate(hashes):
        dlogs = [log for log in logs if hash(json.dumps(log['descriptor'], sort_keys=True)) == dhash]
        encounters = [encounter for log in dlogs for encounter in log['encounters']]
        # There must've been at least one log in order to have an entry in the hashes list
        descriptor = Descriptor.from_json(json.dumps(dlogs[0]['descriptor']))
        expected_color = change_basis(descriptor.expected_pick[1], descriptor.colormodel, descriptor.scalars)

        # Cirlcle the allowed variance for this descriptor
        if len(descriptor.colormodel) == 3:
            # Circle around allowed variance
            r = descriptor.variance
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            x = r * np.outer(np.cos(u), np.sin(v)) + expected_color[0]
            y = r * np.outer(np.sin(u), np.sin(v)) + expected_color[1]
            z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + expected_color[2]
            ax.plot_surface(x, y, z, color="linen", alpha=0.3)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_zlim(0, 1)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_zticklabels([])
            ax.set_xlabel(descriptor.colormodel[0])
            ax.set_ylabel(descriptor.colormodel[1])
            ax.set_zlabel(descriptor.colormodel[2])
            ax.set_title('Shiny picks related to allowed variance')
        else:
            # TODO dim 1 --> numberline (or 2d scatter with y=0)
            # TODO dim 2 --> 2d scatter
            click.echo(f'Plotting a dimension f{len(descriptor.colormodel)} is currently not implemented', err=True)
            return

        for log in dlogs:
            colors = list(map(lambda e: change_basis(e['pick'], descriptor.colormodel, descriptor.scalars), encounters))
            variances = list(map(lambda color: variance(color, expected_color) * (-1 if color < expected_color else 1), colors))
            display_colors = list(map(lambda e: e['pick'], encounters))
            colors = np.transpose(colors)
            ax.scatter(*colors, depthshade=False, c=display_colors)

    plt.show()

