from time import sleep

from nxbt import Nxbt
from nxbt import PRO_CONTROLLER
from random import randint


def random_colour():
    return [randint(0, 255),randint(0, 255),randint(0, 255),]

EXIT_MENU = """
5s
LOOP 3
    B 0.2s
    1.5s
DPAD_UP 0.1s
DPAD_LEFT 2s
A 0.1s
"""

def hunt_shiny(macro):
    """
    Executes a shiny hunt. Will exit when shiny is found.

    macro: An nxbt macro as string. Macros are expected to end exactly when the
    shiny sound should start.

    Basic algorithm:
    - run macro
    - record time to break amplitude threshold
    - time less than threshold -> shiny
    """
    # TODO Make this initialization better
    nx = Nxbt()

    # Get a list of all available Bluetooth adapters
    adapters = nx.get_available_adapters()
    # Prepare a list to store the indexes of the
    # created controllers.
    controller_idxs = []
    # Loop over all Bluetooth adapters and create
    # Switch Pro Controllers
    for i in range(0, len(adapters)):
        index = nx.create_controller(
            PRO_CONTROLLER,
            adapter_path=adapters[i],
            colour_body=random_colour(),
            colour_buttons=random_colour())
        controller_idxs.append(index)

    # Select the last controller for input
    controller_idx = controller_idxs[-1]

    print("Waiting for connection")
    # Wait for the switch to connect to the controller
    nx.wait_for_connection(controller_idx)

    print("Exiting controller menu...")
    macro_id = nx.macro(controller_idx, EXIT_MENU)

    sleep(5)

    print("Shiny hunting...")
    while True:
        macro_id = nx.macro(controller_idx, macro)
        sleep(15)

