#Wild Things Clear
#Helper script
#Version 1.0
#11/17/2019

#Do not tamper with import
import RPi.GPIO as PIN

#Block false errors and set pin layout
PIN.setwarnings(False)
PIN.setmode(PIN.BOARD)

#set GPIO pins for the functional output
#In this version those pins correspond to lights
lightLeft = 12
lightBack = 8
lightRight = 10
#set the pins as GPIO output
PIN.setup(lightLeft, PIN.OUT)
PIN.setup(lightBack, PIN.OUT)
PIN.setup(lightRight, PIN.OUT)
#kill all functional output
PIN.output(lightLeft, PIN.LOW)
PIN.output(lightBack, PIN.LOW)
PIN.output(lightRight, PIN.LOW)

PIN.cleanup()
