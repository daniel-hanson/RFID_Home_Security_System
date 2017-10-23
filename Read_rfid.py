#!/usr/bin/env python

import sys
import signal
import time
import thread
import bluetooth
from pirc522 import RFID
import RPi.GPIO as GPIO

run = True
rfid = RFID()
util = rfid.util()
util.debug = True

bd_addr = "B8:27:EB:3D:BE:73"
port = 1

def ctrlCHandler(signal,frame):
	global run
	run = False
	rfid.cleanup()
	pwm.stop()
	print("\nQuit Program")
	GPIO.cleanup()
	sys.exit()

def receiveFromServer(threadName, delay):
	global pwm
	size = 1024
	while 1:
		try:
			ValidationFlag = s.recv(size)
			print "\nReceived [%s]" % ValidationFlag
			if int(ValidationFlag) == 1:
				print("Activate the servor motor to open the lock")
				DesiredAngle = 180
				DutyCycle = ((DesiredAngle/180.0) + 1.0) * 5.0
				pwm.ChangeDutyCycle(DutyCycle)
				time.sleep(1)
				DesiredAngle = 0.1
				DutyCycle = ((DesiredAngle/180.0) + 1.0) * 5.0
				pwm.ChangeDutyCycle(DutyCycle)
				time.sleep(1)
				
			else:
				print("No further action required")
			
		except:
			print("Server down")

signal.signal(signal.SIGINT, ctrlCHandler)

s=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
s.connect((bd_addr, port))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
pwm=GPIO.PWM(11,50) # pin 11, 50Hz
DesiredAngle = 0.1
DutyCycle = ((DesiredAngle/180.0) + 1.0) * 5.0
pwm.start(DutyCycle)

try:
   thread.start_new_thread(receiveFromServer, ("Thread-1", 2, ) )
except:
   print "Error: unable to start thread"

while run:
	rfid.wait_for_tag()

	(error, data) = rfid.request()
	if not error:
		print("\n\nDetected present tag")
#		print("Backbits: " + format(data, "02x"))

		(error, cardID) = rfid.anticoll()
		if not error:
			cardIdStr = str(cardID[0])+"."+str(cardID[1])+"."+str(cardID[2])+"."+str(cardID[3])+"."+str(cardID[4])
			print("Card ID: "+cardIdStr)
			try:
				s.send(cardIdStr)
			except:
				print("Card ID cannot be sent to the server for validation")

#			print("\nSet tag with tag ID")
#			util.set_tag(cardID)
#
#			print("\nAuthorize the card")
#			key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
#			util.auth(rfid.auth_b, key)
#
#			print("\nReading all sections")
#			for i in range(64):
#				error = util.do_auth(i)
#				if not error:
#					(error, data) = util.rfid.read(i)
#					print(util.sector_string(i) + ": " + str(data))
#
#			print("\nDeauthorize the card")
#			util.deauth()

			print(" ")
			time.sleep(0.5)


