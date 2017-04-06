from sense_hat import SenseHat
from time import sleep
import os

# Constants
SPEED = 0.025

O=[0,0,0]
X=[255,0,0]

connector = [
O, O, O, O, O, O, O, O,
O, O, X, O, X, O, O, O,
O, O, X, O, X, O, O, O,
O, X, X, X, X, X, O, O,
O, X, O, O, O, X, O, O,
O, X, O, O, O, X, O, O,
O, O, X, X, X, O, O, O,
O, O, O, X, O, O, O, O
]

# Commands definition

# Shuts down Raspberry Pi.
DIRECTION_1 = 'down'
TIMES_1 = 3

#Turns off LEDs.
DIRECTION_2 = 'up'
TIMES_2 = 2


sense = SenseHat()
sense.set_rotation(180)

def shutdown():
	'''
	Shuts down Raspberry Pi
	'''
	sense.show_message('Shutting down...', scroll_speed=SPEED, text_colour=[255,0,0])
	sense.set_pixels(connector)
	os.system('sudo shutdown now')
	return

def matrixOff():
	'''
	Turns off LED matrix.
	'''
	sense.show_message('Screen off', scroll_speed=SPEED)
	sense.clear()
	return




# ALL counters should be initialized here.
# Keep in mind when adding more commands.
counter_1 = counter_2 = 1

while True:

	# "emptybuffer=True" so that the first movement after waiting for an event (i.e. pressed),
	# will be recorded instead of the "released" that might have been recorded in the
	# previous iteration.
	event = sense.stick.wait_for_event(emptybuffer=True)
	sleep(0.3)
	print("The joystick was {} {}".format(event.action, event.direction))
	
	
	if (event.direction == DIRECTION_1) and (event.action == 'pressed'):

		if counter_1 == TIMES_1: # number of times the key should be **consecutively** pressed.
			
			counter_1 = 1
			shutdown()
			
		else:
			counter_1 += 1

	
	elif (event.direction == DIRECTION_2) and (event.action == 'pressed'):

		if counter_2 == TIMES_2: # number of times the key should be **consecutively** pressed.
						
			counter_2 = 1
			matrixOff()
			
		else:
			counter_2 += 1

	
	else:

		# Reset ALL commands counters here.
		counter_1 = counter_2 = 1


