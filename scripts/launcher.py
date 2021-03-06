#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi

import time
import Adafruit_CharLCD as LCD
import datetime
import socket
import commands
import shutil
import os


usb0path = "/media/usb0"
usb1path = "/media/usb1"

#-------------------------------------------------------------
# Helper Functions
#-------------------------------------------------------------
def countFiles(directory):
    files = []
 
    if os.path.isdir(directory):
        for path, dirs, filenames in os.walk(directory):
            files.extend(filenames)
 
    return len(files)

def makedirs(dest):
    if not os.path.exists(dest):
        os.makedirs(dest)

def copyFilesWithProgress(src, dest, lcd):
	numFiles = countFiles(src)
 
	if numFiles > 0:
		makedirs(dest)
 
		numCopied = 0
 
		for path, dirs, filenames in os.walk(src):
			for directory in dirs:
				destDir = path.replace(src,dest)
				makedirs(os.path.join(destDir, directory))
            
			for sfile in filenames:
				srcFile = os.path.join(path, sfile)
 
				destFile = os.path.join(path.replace(src, dest), sfile)
                
				shutil.copy(srcFile, destFile)
                
				numCopied += 1
                
				progress = int(round( (numCopied / float(numFiles)) * 100))
				
				lcd.clear()
				msg = u'copy in progress\n{0}/{1}  {2}%'.format(numCopied, numFiles, progress)
				lcd.message(msg)

def printHello(lcd):
	lcd.message('Hello!\n')
	myIp = commands.getoutput("hostname -I")
	lcd.message(myIp)
	# Wait 5 seconds
	time.sleep(2.0)
	lcd.clear()

#-------------------------------------------------------------
# Main Task
#-------------------------------------------------------------

# raspbpberry Pi pin setup
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
lcd.clear()

printHello(lcd)

try:
	lastIP = ""
	copied = 0
	while 1:
		firstline = time.strftime("%d.%m.%y %H:%M")
		secondline = ""


		myIp = commands.getoutput("hostname -I")
		if lastIP != myIp:
			lastIP = myIp;
			output = firstline +"\n" + myIp
			lcd.clear()
			lcd.message(output)
			time.sleep(3);

		usb0 = 0
		usb1 = 0
		if os.path.ismount(usb0path):
			secondline += " usb0"
			usb0 = 1

		if os.path.ismount(usb1path):
			secondline += " usb1"
			usb1 = 1

		lcd.clear()
		output = firstline +"\n" + secondline
		lcd.message(output)
		time.sleep(1.0)

		if usb0 & usb1 & (copied == 0):
			try:
				lcd.clear()
				lcd.message("copy starting")
				time.sleep(3.0)
				copyFilesWithProgress(usb1path, usb0path, lcd)

				lcd.clear()
				lcd.message("copy finished\nremove the stick")
				time.sleep(10.0)
				printHello(lcd)
			except BaseException  as e: 
				lcd.clear()
				lcd.message("OOPS ERROR...\n{}".format(e))
				time.sleep(10.0)
			copied = 1
		else:
			if usb0 & usb1:
				copied = copied
			else:
				copied = 0

except BaseException  as e: 
	copied=10

lcd.clear()
lcd.message("Bye Bye...")

lcd.clear()

