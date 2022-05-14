import click

from .describe import describe
from .detect import detect
from .execute import execute
from .pick import pick
from .record import record
from .variance import variance

@click.group()
def cli():
    pass

cli.add_command(describe)
cli.add_command(detect)
cli.add_command(execute)
cli.add_command(pick)
cli.add_command(record)
cli.add_command(variance)


if __name__ == '__main__':
    cli()

