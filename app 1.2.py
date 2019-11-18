# Wild Things Head Array
# Main script
# Version 1.2
# 11/17/2019

# Do not change any of the imports
import RPi.GPIO as PIN
import time as t
# I've disabled  false errors and set the configuration for the GPIO pin layout
# warnings
PIN.setwarnings(False)
# pin layout
PIN.setmode(PIN.BOARD)


def Main():
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
	kill = 25
	PIN.setup(kill, PIN.IN)
	killCommand = False

	# Initialize the restart switch
	restart = 27
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
		t.sleep(0.5)
		# kill all functional output
		PIN.output(lightLeft, PIN.LOW)
		PIN.output(lightBack, PIN.LOW)
		PIN.output(lightRight, PIN.LOW)

	# kill all functional output
	PIN.output(lightLeft, PIN.LOW)
	PIN.output(lightBack, PIN.LOW)
	PIN.output(lightRight, PIN.LOW)
	# Deactivate pins and clear all active function
	PIN.cleanup()

	if restartCommand:
		print("Restarting...")
		Main()
	return


def filters(timeSide):
	timeTot = 10
	if timeSide > timeTot:
		delay = 0
		return delay
	delay = timeTot - timeSide
	return delay
