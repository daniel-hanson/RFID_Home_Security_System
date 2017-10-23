#!/usr/bin/env python

import sys
import signal
import time
import thread
import bluetooth
import cv2
from PIL import Image
import numpy as np
import mysql.connector as mariadb
import matplotlib
from PIL import Image


def ctrlCHandler(signal,frame):
	print("Closing socket")
	client_sock.close()
	server_sock.close()
	cursor.close()
	mariadb_connection.close()
	print("Quit Program")
	sys.exit()

def cameraListener(threadName, delay):
	global ValidationFlag
	global TakePictureFlag
	size = 1024
	cam_client_sock, cam_address = server_sock.accept()
	print(cam_address[0])
	while 1:
		
		if int(ValidationFlag) == 0:
			print("Thread: ValidationFlag = 0")
			TakePictureFlag = "1"
			cam_client_sock.send(TakePictureFlag)

			for i in range(3):
				img_height = cam_client_sock.recv(size)
				img_width = cam_client_sock.recv(size)
				img_channels = cam_client_sock.recv(size)
				cam_data_size = cam_client_sock.recv(size)

				stringData = ""
				while int(cam_data_size) != len(stringData):
					stringData += cam_client_sock.recv(size)
			
				print("Height: " + img_height + "  Width: " + img_width + "  Channels: " + img_channels)
				print ("Received image string length: " + cam_data_size)
				#print("Image string: \n" + stringData)
				print ("Actual image string length: " + str(len(stringData)))

				img_str = np.fromstring(stringData, np.uint8)
				img = cv2.imdecode(img_str, cv2.IMREAD_COLOR)

				file = "/home/pi/test_image_" + str(i) + ".png"
				cv2.imwrite(file, img)

			TakePictureFlag = "-1"
			ValidationFlag = "-1"
		else:
			time.sleep(1)
			


signal.signal(signal.SIGINT, ctrlCHandler)

mariadb_connection = mariadb.connect(user='pi', password='raspberry', database='RFID_Home_Security')
cursor = mariadb_connection.cursor()

server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1
size = 1024

#cam_bd_addr = "B8:27:EB:B8:06:2C"

server_sock.bind(("",port))
server_sock.listen(1)

client_sock, address = server_sock.accept()

try:
   thread.start_new_thread(cameraListener, ("Thread-1", 2, ) )
except:
   print "Error: unable to start thread"

cardIdString = None
ValidationFlag = "-1"
TakePictureFlag = "-1"

while 1:
	
	try:
		print(address[0])
		data = client_sock.recv(size)
		print "\n\nReceived [%s]" % data
		cardIdString = None

		cursor.execute("SELECT cardid FROM RFID_Capstone WHERE cardid=%s", (data,))
		for cardid in cursor:
			cardIdString = str(cardid).split("'")
			print("Card ID: "+ cardIdString[1])

		if cardIdString is None:
			ValidationFlag = "0"
			#client_sock.send(ValidationFlag)
			#print("ValidationFlag = 0 Sent")
	
		else:
			if data == cardIdString[1]:
				ValidationFlag = "1"
				client_sock.send(ValidationFlag)
				print("ValidationFlag = 1 Sent")
				ValidationFlag = "-1"
			else:
				ValidationFlag = "0"
				#client_sock.send(ValidationFlag)
				#print("ValidationFlag = 0 Sent")
	except:
		print("Client down")
		time.sleep(5)






