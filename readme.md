# Build
## Arduino
```
$ arduino-cli board list
Port         Protocol Type              Board Name  FQBN            Core
/dev/ttyACM0 serial   Serial Port (USB) Arduino Uno arduino:avr:uno arduino:avr

$ arduino-cli compile --fqbn arduino:avr:uno microphone
$ arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno microphone
```

# Debugging
- I had a lot of trouble getting a stock Raspberry Pi 4 to reliably make a
  connection with `nxbt`. While it broke wifi connectivity, installing
  `connman` seemed to resolve this issue.
- Running `systemctl stop bluetooth.service` then starting the script worked
  well as well.

# Dependancies

- [nxbt](https://github.com/Brikwerk/nxbt)
- pydub

# Assets
- [BDSP Shiny Sound](./assets/bdsp-shiny.wav) by [Testostyronne on Youtube](https://www.youtube.com/channel/UCqebtkAws3kAgzr5_N2x9BQ) - [video](https://www.youtube.com/watch?v=tx1_cgdkppU)

