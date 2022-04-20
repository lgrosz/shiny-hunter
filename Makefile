arduino: a-build a-upload

a-build:
	arduino-cli compile --fqbn arduino:avr:uno microphone

a-upload:
	arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno microphone

a-monitor:
	arduino-cli monitor -p /dev/ttyACM0 -l serial -b arduino:avr:uno -c baudrate=115200
