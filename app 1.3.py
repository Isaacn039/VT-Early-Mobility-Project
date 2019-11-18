# Wild Things Head Array
# Main script
# Version 1.3
# 11/17/2019

# This file is the main script for the VT Early Mobility Project Wild Thing unit
# The script starts the sensors on the head array, reads the input, and controls the functional output commands
# This file and all others in the VT Early Mobility Project

# Do not change any of the imports
import RPi.GPIO as PIN
import time as t
# I've disabled  false errors and set the configuration for the GPIO pin layout
# warnings
PIN.setwarnings(False)
# pin layout
PIN.setmode(PIN.BOARD)


def Main():
	# This function sets all of the input/output pin numbers, reads sensor input, calculates which sensor is closest to
	# to the patient's head, and sends commands to the lights corresponding to the three directions

	# pin layout
	PIN.setmode(PIN.BOARD)

	print("Initializing")
	# Set the GPIO pins for the sensor output
	trigLeft = 3
	trigBack = 5
	trigRight = 19
	# Set the GPIO pins for the sensor input
	echoRight = 11
	echoLeft = 13
	echoBack = 15
	# Set the GPIO pins for the functional output
	lightBack = 8
	lightRight = 10
	lightLeft = 12
	# These lights correspond to the motors that would be activated

	# Initialize the Kill switch
	kill = 29
	PIN.setup(kill, PIN.IN)
	killCommand = False

	# Initialize the restart switch
	restart = 31
	PIN.setup(restart, PIN.IN)
	restartCommand = False

	# Initialize all of the pins for input, output, and function
	PIN.setup(trigLeft, PIN.OUT)
	PIN.setup(trigBack, PIN.OUT)
	PIN.setup(trigRight, PIN.OUT)

	PIN.setup(echoLeft, PIN.IN)
	PIN.setup(echoBack, PIN.IN)
	PIN.setup(echoRight, PIN.IN)

	PIN.setup(lightLeft, PIN.OUT)
	PIN.setup(lightBack, PIN.OUT)
	PIN.setup(lightRight, PIN.OUT)
	# Let the raspberry pi pause for a moment to start the sensors
	t.sleep(0.1)
	print("Sensors Starting Up...")
	# Sensors started

	# This statement is only True when the kill switch has not been activated
	# Kill switch added in version 1.2
	while not killCommand:
		# Left
		# Sensor output
		PIN.output(trigLeft, PIN.HIGH)
		t.sleep(0.00001)
		PIN.output(trigLeft, PIN.LOW)

		# sensor input
		while PIN.input(echoLeft) == 0:
			pass
		startLeft = t.time()

		while PIN.input(echoLeft) == 1:
			pass
		stopLeft = t.time()
		timeLeft = stopLeft - startLeft

		# Back
		PIN.output(trigBack, PIN.HIGH)
		t.sleep(0.00001)
		PIN.output(trigBack, PIN.LOW)

		while PIN.input(echoBack) == 0:
			pass
		startBack = t.time()

		while PIN.input(echoBack) == 1:
			pass
		stopBack = t.time()
		timeBack = stopBack - startBack

		# Right
		PIN.output(trigRight, PIN.HIGH)
		t.sleep(0.00001)
		PIN.output(trigRight, PIN.LOW)

		while PIN.input(echoRight) == 0:
			pass
		startRight = t.time()

		while PIN.input(echoRight) == 1:
			pass
		stopRight = t.time()
		timeRight = stopRight - startRight

		# Calculate the distances from each sensor to the patient
		disLeft = (timeLeft * 17000)
		disBack = (timeBack * 17000)
		disRight = (timeRight * 17000)
		# Print the distances
		print("Left:")
		print(disLeft)
		print("Back:")
		print(disBack)
		print("Right:")
		print(disRight)

		# Determine which sensor is being triggered
		# The sensor closest to the patient should trigger
		if disLeft < disBack and disLeft < disRight:
			print("moving Left")
			PIN.output(lightLeft, PIN.HIGH)
		elif disBack < disLeft and disBack < disRight:
			print("moving Back")
			PIN.output(lightBack, PIN.HIGH)
		elif disRight < disLeft and disRight < disBack:
			print("moving Right")
			PIN.output(lightRight, PIN.HIGH)
		if PIN.input(kill) == 1:
			killCommand = True
		t.sleep(0.5)
		# kill all functional output
		PIN.output(lightLeft, PIN.LOW)
		PIN.output(lightBack, PIN.LOW)
		PIN.output(lightRight, PIN.LOW)

	# kill all functional output
	PIN.output(lightLeft, PIN.LOW)
	PIN.output(lightBack, PIN.LOW)
	PIN.output(lightRight, PIN.LOW)
	print("Stopping...")
	# Deactivate pins and clear all active function
	# PIN.cleanup()

	while not restartCommand:
		if PIN.input(31) == 1:
			print("Restarting...")
			restartCommand = True
		if PIN.input(29) == 1:
			print("Exit")
			PIN.output(lightLeft, PIN.LOW)
			PIN.output(lightBack, PIN.LOW)
			PIN.output(lightRight, PIN.LOW)
			PIN.cleanup()
	t.sleep(0.5)
	Main()
	return


def filters(timeSide):
	# This function takes in the response time obtained for one of the sensors on the head array
	# this time is then used to calculate the delay, or the amount of time the main function should pause before
	# triggering the next sensor output
	timeTot = 10
	if timeSide > timeTot:
		delay = 0
		return delay
	delay = timeTot - timeSide
	return delay


Main()
