# Build
No build, just run the python scripts.

# Dependancies

- [nxbt](https://github.com/Brikwerk/nxbt)
- pyaudio

# Usage
## Sample recorder
The usage of the sample recorder should be self-explanitory. Simply run
`python3 SampleRecorder.py` and follow the prompts. It should exit relatively
gracefully via a keyboard interrupt.

The sample recorder saves `.wav` files to the current working directory as
`<uuidv1>.wav`. This meant they should be time-sortable.

## Shiny hunter
Not worth writing the docs on this poorly working prototype, just read the
code.

# Common issues
- I had a lot of trouble getting a stock Raspberry Pi 4 to reliably make a
  connection with `nxbt`. While it broke wifi connectivity, installing
  `connman` seemed to resolve this issue.
- Running `systemctl stop bluetooth.service` then starting the script worked
  well as well.

