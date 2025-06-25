import sys
sys.path.append('/home/pi/TurboPi/')


import time
import HiwonderSDK.Board as Board

def imperial_walk():
	
	short = 0.2/1.5 
	medium = 0.4/1.5
	longs = 0.6/1.5
	pause = 0.2/1.5
	
	def beep(duration):
		Board.setBuzzer(1)
		time.sleep(duration)
		Board.setBuzzer(0)
		
		if duration == short:
			time.sleep(pause/2)
		else:
			time.sleep(pause)
	for i in range(2):
		beep(longs)
		beep(longs)
		beep(longs)
		beep(medium)
		beep(short)
		beep(longs)
		beep(medium)
		beep(short)
		beep(longs) 
		time.sleep(longs*1.5)
		
		
	beep(longs)
	beep(medium)
	beep(short)
	beep(longs)
	beep(medium)
	beep(short)
	beep(short)
	beep(short)
	beep(short)
	
	time.sleep(longs*1.5)
	
	beep(short)
	beep(longs)
	beep(medium)
	beep(short)
	beep(short)
	beep(short)
	beep(short)
	
	time.sleep(1.5*longs)
		
	beep(short)
	beep(longs)
	beep(medium)
	beep(short)
	beep(longs)
	beep(medium)
	beep(short)
	beep(longs)
	
	time.sleep(longs*1.5)
	# c
	beep(longs)
	beep(medium)
	beep(short)
	beep(longs)
	beep(medium)
	beep(short)
	beep(short)
	beep(short)
	beep(short)
	
	time.sleep(longs*1.5)
	
	beep(short)
	beep(longs)
	beep(medium)
	beep(short)
	beep(short)
	beep(short)
	beep(short)
	
	time.sleep(1.5*longs)
	
	beep(short)
	beep(longs)
	beep(medium)
	
	beep(short)
	beep(longs)
	beep(medium)
	beep(short)
	beep(longs)

	
	
#Board.setBuzzer(0)

#time.sleep(1)

#Board.setBuzzer(1)
#time.sleep(0.5)
#Board.setBuzzer(0)
