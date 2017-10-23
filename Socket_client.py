#!/usr/bin/env python

import sys
import signal
import time
import thread
import bluetooth
import cv2
import numpy as np

def ctrlCHandler(signal,frame):
	global camera
	global s
	s.close()
	del(camera)
	print("\nQuit Program")
	sys.exit()

def get_image():
	retval, im = camera.read()
	return im

bd_addr = "B8:27:EB:3D:BE:73"
port = 1
size = 1024

cameraID = 0
num_frames = 30

signal.signal(signal.SIGINT, ctrlCHandler)

s=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
s.connect((bd_addr, port))

camera = cv2.VideoCapture(cameraID)

while 1:
	TakePictureFlag = s.recv(size)
	print "\n\nReceived [%s]" % TakePictureFlag

	if int(TakePictureFlag) == 1:
		for i in xrange(num_frames):
			temp_im = get_image()

		for i in range(3):
			camera_capture = get_image()
			#cv2.imwrite("test_image.png", camera_capture)

			img_height, img_width, img_channels = camera_capture.shape
			print("Height: " + str(img_height) + "  Width: " + str(img_width) + "  Channels: " + str(img_channels))

			img_str = cv2.imencode('.jpg', camera_capture)[1].tostring()
			print ("Image string length: " + str(len(img_str)))
			#print("Image string: \n" + img_str)

			s.send(str(img_height));
			s.send(str(img_width));
			s.send(str(img_channels));
			s.send(str(len(img_str)));
		
			count = 0
			while len(img_str)-count > 1000:
				s.send(img_str[0+count:0+count+1000])
				count = count + 1000
				#print("Sending img_str")

			s.send(img_str[0+count:])
			#print("Sending img_str")

			print("Complete sending img_str")
			count = 0

			time.sleep(5)

	else:
		print("No further action required")


s.close()


