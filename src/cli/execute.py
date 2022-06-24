from os import environ
from time import sleep, strftime
import click
import json

from api.descriptor import Descriptor
from api.detect import detect
from api.pick import pick
from api.variance import variance as aVariance
from api.change_basis import Bases


RESET_PIN = 17

@click.option('--variance', type=float, help='Override the descriptor color variance by setting this. This will only apply to the final shiny pick. The resolvers variance are locked to 0.1.')
@click.option('--colormodel',
              type=click.Choice(Bases),
              help='Override the descriptor colormodel by setting this.')
@click.option('--scalar', 'scalars',
              type=str,
              multiple=True,
              help='Override the descriptor scalars by setting these.')
@click.option('--debounce', type=int, default=0, help='Second to debounce the identifier resolver after a (non)shiny pick')
@click.option('--controller-pin', type=str, help=f'Pin of a raspberry pi which to flag the controller. Its IP should be set via the environment variable PIGPIO_ADDR. Pin gets pulled low to indicate shiny')
@click.argument('file', default='-', type=click.File('r'))
@click.command(help='Records a shiny detector package. Saves to file.')
def execute(variance, colormodel, scalars, debounce, controller_pin, file):
    descriptor = Descriptor.from_json(file.read())

    # CLI overrides
    if variance is not None:
        descriptor.variance = variance

    if colormodel is not None:
        descriptor.colormodel = colormodel

    if len(scalars) != 0:
        descriptor.scalars = scalars

    resets = 0
    found = False

    encounterLogs = []

    notifier = None
    if controller_pin is not None and environ.get('PIGPIO_ADDR') is not None:
        from gpiozero import DigitalOutputDevice
        notifier = DigitalOutputDevice(controller_pin, active_high=False)
        click.echo(f'Setup notifier at {environ.get("PIGPIO_ADDR")} pin {controller_pin}')

    while not found:
        try:
            logdata = {
                'encounter': resets,
                'time': strftime("%Y%m%d-%H%M%S"),
                'resolvers': [],
                'pick': None
            }
            click.echo('Resolving identifers...')
            for i in descriptor.resolvers:
                pos, color = i
                c = detect(pos, color, descriptor.colormodel, descriptor.scalars, 0.1)
                logdata['resolvers'].append(c)

            click.echo('Delaying for shiny pick...')
            sleep(descriptor.pick_delay)

            shiny_loc, shiny_color = descriptor.expected_pick
            picked_color = pick(*shiny_loc)
            click.echo(f'Picked {picked_color}')

            logdata['pick'] = picked_color
            encounterLogs.append(logdata)
            if (aVariance(picked_color, shiny_color) > descriptor.variance):
                found = True
                if notifier is not None:
                    notifier.on()
            else:
                click.echo('Not shiny')
                resets += 1
                sleep(debounce)
        except KeyboardInterrupt:
            click.echo('Interrupted by user', err=True)
            break

    if (found):
        click.echo(f'Found shiny in {resets} resets.')

    with open(f'cli-execute_{strftime("%Y%m%d-%H%M%S")}.json', 'w') as f:
        json.dump({
            'descriptor': json.loads(descriptor.to_json()),
            'encounters': encounterLogs
        }, f)

