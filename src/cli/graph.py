import click

from .graph_huevencounter import hue_v_encounter
from .graph_variance_scatter import variance_scatter


@click.group(help='Common graphs to visual hunts from execute logs')
def graph():
    pass

graph.add_command(hue_v_encounter)
graph.add_command(variance_scatter)

