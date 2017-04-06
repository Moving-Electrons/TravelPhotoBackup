#!/usr/bin/python3

import os
import sys
from sh import rsync
from datetime import datetime
from time import sleep
from sense_hat import SenseHat

		

def create_folder(path):
	'''
	Checks if the destination folder is present in the destination drive.
	If it's not, it attempts to create it.
	'''

	print ('attempting to create destination folder: ',path)
	if not os.path.exists(path):
		try: 
			os.mkdir(path)
			print ('Folder created.')
		except:
			print ('Folder could not be created. Stopping.')
			return
	else:
		print ('Folder already in path. Using that one instead.')


def read_configuration():
	'''
	Reads the script configuration file.
	'''

	try:
		
		with open(CONFIG_FILE, 'rU') as file: #IMPORTANT: rU Opens the file with Universal Newline Support, so \n and/or \r is recognized as a new line. 

			confList = file.readlines()

			for line in confList:
				line = line.strip('\n')

				try:
					name , value = line.split('=')

					if name.strip() == 'mount folder': #.strip eliminates leading and ending spaces only.
						mount_path = value.strip()
					elif name.strip() == 'destination folder':
						dest_path = value.strip()


				except ValueError:
					print ('Incorrect line format in configuration file.\nExiting.')
					camera_graph('red')
					sys.exit(1)

	except FileNotFoundError:

		print ('Error: File not found!.')
		camera_graph('red')
		sys.exit(1)
	
	return (mount_path, dest_path)


def camera_graph(color='white'):
	'''
	It generates the "camera graph" in the LED matrix.
	'''
		
	# uncomment below if global variable "sense" will be modified.
	#global sense

	O = [0, 0, 0] # LEDs off.
	colors = {
	'green': [0,255,0],
	'red' : [255,0,0],
	'white' : [255,255,255]
	}	

	
	if color in colors:

		C = colors[color]

		camera_small = [
		O, O, O, O, O, O, O, O,
		O, O, O, C, C, O, O, O,
		O, C, C, O, O, C, C, O,
		O, C, O, C, C, O, C, O,
		O, C, O, C, C, O, C, O,
		O, C, C, C, C, C, C, O,
		O, O, O, O, O, O, O, O,
		O, O, O, O, O, O, O, O
		]

		sense.set_pixels(camera_small)

	else:

		print ('bad argument. Color not in list.')

def led_message():

	sense.show_message



if __name__ == '__main__':

	'''
	This script copies a mounted SD Card to a folder automatically 
	created with the same SD Card's name in the destination drive. 
	The destination drive's folder and the mounting point are defined 
	in the .conf file.

	1 argument:  label/name of the mounted SD Card.
	'''

	# Setting up SenseHat object.
	sense = SenseHat()
	sense.set_rotation(180)

	CONFIG_FILE = '/home/pi/scripts/photos/backup_photos.conf'
	SPEED = 0.03


	try:
		ORIGIN_DEV = sys.argv[1]
	except IndexError:
		print ('Error: Argument missing.\nUsage: python3 backup_photos.py <sd card label>\
			\nExiting.')
		
		camera_graph('red')

		sys.exit(1)


	# Reads configuration file and assigns variables.
	mountFolder, destDevice = read_configuration()

	# Verifying if both origin and destination folders are mounted points. 
	# os.path.exists() can also be used.
	if os.path.ismount(os.path.join(mountFolder,destDevice)) and os.path.ismount(os.path.join(mountFolder,ORIGIN_DEV)):

		#destFolder = mountFolder+destDevice+'/'+ORIGIN_DEV
		destFolder = os.path.join(mountFolder,destDevice,ORIGIN_DEV)


		create_folder(destFolder)

		sense.show_message('Initiating backup...', scroll_speed=SPEED)
		camera_graph()
			
		print (datetime.now().strftime('%Y-%m-%d %H:%M')+' Backup process initiated...')
		
		# Comment out to delete files that are not in the origin:
		# rsync("-av", "--delete", mountFolder+ORIGIN_DEV, destFolder)
		rsync("-av", mountFolder+ORIGIN_DEV+'/', destFolder)
		
		print (datetime.now().strftime('%Y-%m-%d %H:%M')+' Backup process finished.')

		camera_graph('green')


	else:
		print ("Error with mounted drives. Possible issues:\na) Origin drive "+mountFolder+ORIGIN_DEV+" is not mounted.\
			\nb) Destination drive "+mountFolder+destDevice+" is not mounted.\
			\nc) SD Card has a different name.")

		camera_graph('red')
		


