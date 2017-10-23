# RFID_Home_Security_System
(Fall 2017) [ECE 4970W Senior Capstone Design] {Final Project} Tested on Raspberry Pi 3

<br>
<br>

Requirements:
1) Pybluez @https://github.com/karulis/pybluez
2) pi-rc522 @https://github.com/ondryaso/pi-rc522
3) OpenCV @https://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html

<br>

Modules:
1) Central Hub: Check_rfid.py
2) RFID Module: Read_rfid.py
3) Camera Module: Socket_client.py

<br>

Run code when power the Raspberry Pi on:
1) sudo crontab -e
2) Add "@reboot python {directory to the python file} &" at the end of the file

<br>

Raspberry Pi power on sequence: Central Hub -> RFID Module -> Camera Module

<br>

