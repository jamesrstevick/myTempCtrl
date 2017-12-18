Arduino Controlled Benchmark myTemp Temperature Chamber
Written for Python 3
Clarity Movement Co.
James Stevick

----------------------------------------


HARDWARE SETUP:

Start setup with Benchmark myTemp OFF
1. Connect Arduino to computer (powered usb)
2. Wait 10 seconds
3. Turn on Benchmark myTemp
4. Make sure "Set" is not on Temp or Time
5. Send CMDs from Python

----------------------------------------


PYTHON:

Add functions to python script mytemp_program.py

Include python library and class:
- lib_mytemp.py
- mytemp_control.py

set_temp( temp ):
	Sets the temperature of the myTemp chamber
	Input: temp - Temperature [degrees C] between 0.0 and 60.0

set_time( time ):
	Sets the time of the myTemp chamber
	Input: time - Time [minutes] between 0 and 9999

change_settings( temp_or_time , inc_or_dec , num )
	Increases or decreases the temperature or time of the myTemp chamber
	Inputs: temp_or_time - 1 for temperature, 0 for time
		inc_or_dec - 1 for increasing, 0 for decreasing
		num - Amount to increase or decrease the temperature or time

reset_temp():
	Sets the temperature to 0.0 [degrees C]

reset_time():
	Sets the time to 0 [minutes]

press_set( num ):
	Presses the Set button on the myTemp chamber
	input: num - Number of times to press button, default is 1

press_shift( num ):
	Presses the Shift button on the myTemp chamber
	input: num - Number of times to press button, default is 1

press_dec( num ):
	Presses the Decrease button on the myTemp chamber
	input: num - Number of times to press button, default is 1

press_inc( num ):
	Presses the Increase button on the myTemp chamber
	input: num - Number of times to press button, default is 1

----------------------------------------


ARDUINO:

Arduino simulates pressing 1 of 4
myTemp buttons upon receiving CMDs:
-Set: \x53\x45
-Shift: \x53\x48
-Decrease: \x53\x44
-Increase: \x53\x49

