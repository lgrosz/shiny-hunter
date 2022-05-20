import click
from threading import Thread

from api.detect import detect as aDetect

@click.command(help='Detect color at screen position')
@click.option('--pos', type=int, nargs=2, required=True, help='x y position for pixel on screen.')
@click.option('--color', type=float, nargs=3, required=True, help='r g b color for pixel.')
@click.option('--variance', type=float, default=0, help='Allowed color variance.')
def detect(pos, color, variance):
    click.echo('Waiting...')
    thread = Thread(target=aDetect, args=(pos, color, variance))
    thread.start()
    thread.join()

