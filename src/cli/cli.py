import click

from .convert import convert
from .describe import describe
from .detect import detect
from .execute import execute
from .optimize_variance import optimize_variance
from .pick import pick
from .record import record
from .variance import variance
from .fix_pick import fix_expected
from .graph import graph

@click.group()
def cli():
    pass

cli.add_command(describe)
cli.add_command(detect)
cli.add_command(execute)
cli.add_command(pick)
cli.add_command(record)
cli.add_command(variance)
cli.add_command(convert)
cli.add_command(optimize_variance)
cli.add_command(fix_expected)
cli.add_command(graph)


if __name__ == '__main__':
    cli()

