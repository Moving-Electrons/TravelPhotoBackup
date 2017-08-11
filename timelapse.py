import click
import time
import subprocess
from sense_hat import SenseHat



def updateMatrix(pic_number, frames):
	"""
	Updates SenseHAT matrix as photos are taken.
	For the matrix graph to be accurate, the number of frames 
	should be above 8.
	"""

	red = (255, 0, 0)
	green = (0, 255, 0)
	blue = (0, 0, 255)
	white = (255,255,255)

	step = frames/8
	position = int(pic_number/step)

	# Sets current matrix position white unless
	# it's the very last frame. In which case it's 
	# set green.
	if pic_number == frames:
		sense.set_pixel(7,2, green)
		sense.set_pixel(7,3, green)
		sense.set_pixel(7,4, green)
		sense.set_pixel(7,5, green)
	else:
		sense.set_pixel(position,2, white)
		sense.set_pixel(position,3, white)
		sense.set_pixel(position,4, white)
		sense.set_pixel(position,5, white)

	previous = position - 1
	
	# Sets the previous matrix column green.
	if previous >= 0: 
		sense.set_pixel(previous,2, green)
		sense.set_pixel(previous,3, green)
		sense.set_pixel(previous,4, green)
		sense.set_pixel(previous,5, green)

def capturePhotos(delay_secs, no_hat, frames, interval):
	"""
	Initiated time-lapse per parameters specified on each command.
	"""

	time.sleep(delay_secs)		
	for i in range(frames):
		pic = i + 1
		# LED matrix is updated only if the no_hat flag is False (default).
		if not no_hat: 
			updateMatrix(pic, frames) 
		subprocess.call(['gphoto2', '--capture-image-and-download', '--filename', 'timelapse-%Y-%m-%dT%H%M%S.%C'])
		time.sleep(interval)



@click.group()
def timelapse():
	pass


@timelapse.command()
@click.option('--clip_length', help='Final clip length in seconds.', type=int)
@click.option('--event_duration', help='Event duration in minutes', type=int)
@click.option('--delay', help='Delay before initiating timelapse in minutes (default=0).', type=int, default = 0)
@click.option('--fps', help='Final clip frames per second (default=30).', type=int, default=30)
@click.option('--no_hat', help='Do NOT use Sense Hat to show progress (default=False).', is_flag=True, default=False)
def by_clip_length(clip_length, event_duration, delay, fps, no_hat):
	"""
	Calculates timelapse variables based on final clip length and event duration.
	"""
	
	#Uncomment below and modify accordingly to make the script interactive:
	#clip_length = click.prompt('Enter Clip Length (seconds)', type=int)
	#event_duration = click.prompt('Enter Event Duration (minutes)', type=int)
	#delay = click.prompt('Enter Delay (minutes)', default=0)
	#fps = click.prompt('Enter Clip FPS', default=30)

	total_photos = (clip_length * fps)
	event_secs = (event_duration * 60)
	delay_secs = (delay * 60)
	interval = int(event_secs/total_photos)


	print('Total number of pictures: {}'.format(total_photos))
	print('Time interval between pictures (seconds): {}'.format(interval))
	print('Not using Sense HAT: {}'.format(no_hat))
	print('Delaying timelapse for {} seconds'.format(delay_secs))

	capturePhotos(delay_secs, no_hat, total_photos, interval)
	

@timelapse.command()
@click.option('--interval', help='Interval length between photos in seconds.', type=int)
@click.option('--total_photos', help='Number of photos to be taken.', type=int)
@click.option('--delay', help='Delay before initiating timelapse in minutes (default=0).', type=int, default = 0)
@click.option('--fps', help='Final clip frames per second (default=30).', type=int, default=30)
@click.option('--no_hat', help='Do NOT use Sense Hat to show progress (default=False).', is_flag=True, default=False)
def by_interval_length(interval, total_photos, delay, fps, no_hat):
	"""
	Calculates total time and approximate clip length.
	"""

	event_mins = (interval * total_photos)/60
	delay_secs = (delay * 60)
	clip_length = (total_photos / fps)

	print('Event duration (minutes): {}'.format(event_mins))
	print('Final clip length (seconds): {}'.format(clip_length))
	print('Not using Sense HAT: {}'.format(no_hat))
	print('Delaying timelapse for {} seconds'.format(delay_secs))
	print('=====================================')

	capturePhotos(delay_secs, no_hat, total_photos, interval)
	

if __name__ == '__main__':

	sense = SenseHat()
	
	# Uncomment for brighter LED Matrix.
	sense.low_light = True
	timelapse()
	sense.low_light = False



