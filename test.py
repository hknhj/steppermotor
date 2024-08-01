import RPi.GPIO as GPIO
import time
import threading
from DRV8825 import DRV8825

def printOption():
	print('1. Move to specific location')
	print('2. Move in a cycle')
	option = int(input('Enter option: '))
	return option
	
def initMotor():
	print('init motor...')
	
def moveMotor(direction, steps):
	smooth = 30
	Motor1.TurnStep(Dir=direction, steps=steps, stepdelay=0.0015)
	'''Motor1.TurnStep(Dir=direction, steps=30, stepdelay=0.0015)'''
	

def moveToSpecificLoc(cur_loc):
	location = int(input(f'Enter specific location (1 - 4) (current: {cur_loc}) : '))
	
	if location == 5:
		return 5
		
	pulse = 600
	steps = abs(location-cur_loc) * pulse
	
	if location - cur_loc > 0:
		moveMotor('forward', steps)
	elif location - cur_loc < 0:
		moveMotor('backward', steps)
	else:
		print('Current location is same with the entered location')
		
	return location
				
	
def moveInCycle():
	print('move in a cycle')

def doingJob(motor):
	motor.TurnStep(Dir='forward', steps=800, stepdelay=0.001)
	time.sleep(0.5)
	motor.TurnStep(Dir='backward', steps=800, stepdelay=0.001)
	motor.Stop()
	

try:
	Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
	Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
	
	GPIO.setmode(GPIO.BCM)
	
	GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	
	try:
		while True:
			switch_12_state = GPIO.input(12)
			switch_13_state = GPIO.input(13)
			
			if switch_12_state == GPIO.LOW:
				print("switch 12 pushed")
			else:
				print("switch12 not pushed")
			
			if switch_13_state == GPIO.LOW:
				print("switch 13 pushed")
			else:
				print("switch 13 not pushed")
				
			time.sleep(1)
			
	finally:
		GPIO.cleanup()

	"""
	# 1.8 degree: nema23, nema14
	# 200 steps to rotate a circle
	# softward Control :
	# 'fullstep': A cycle = 200 steps
	# 'halfstep': A cycle = 200 * 2 steps
	# '1/4step': A cycle = 200 * 4 steps
	# '1/8step': A cycle = 200 * 8 steps
	# '1/16step': A cycle = 200 * 16 steps
	# '1/32step': A cycle = 200 * 32 steps
	Motor1.TurnStep(Dir='backward', steps=4800, stepdelay = 0.001)
	"""
	'''
	Motor1.SetMicroStep('softward','1/16step')
	
	initMotor()
	cur_loc = 1
	
	Motor1.TurnStep(Dir='forward', steps=2400, stepdelay = 0.001)
	while(True):
		option = printOption()
		if option==1:
			while(True):
				if cur_loc==5:
					break
				cur_loc = moveToSpecificLoc(cur_loc)
		elif option==2:
			while(True):
				moveInCycle()
		else:
			print('Wrong option. Enter 1 or 2')
	'''

	"""
	# 28BJY-48:
	# softward Control :
	# 'fullstep': A cycle = 2048 steps
	# 'halfstep': A cycle = 2048 * 2 steps
	# '1/4step': A cycle = 2048 * 4 steps
	# '1/8step': A cycle = 2048 * 8 steps
	# '1/16step': A cycle = 2048 * 16 steps
	# '1/32step': A cycle = 2048 * 32 steps
	"""
	Motor1.SetMicroStep('softward' ,'1/8step')    
	Motor2.SetMicroStep('softward' ,'1/8step')  
	
	'''
	thread1 = threading.Thread(target=doingJob, args = (Motor1,))
	thread2 = threading.Thread(target=doingJob, args = (Motor2,))
	
	thread1.start()
	thread2.start()
	'''
	'''
	Motor1.TurnStep(Dir='forward', steps=200, stepdelay=0.001)
	time.sleep(0.5)
	Motor1.TurnStep(Dir='backward', steps=200, stepdelay=0.001)
	Motor1.Stop()
	'''
	'''
	  
	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=0.001)
	time.sleep(0.5)
	Motor2.TurnStep(Dir='backward', steps=200, stepdelay=0.001)
	Motor2.Stop()
	'''


	'''Motor1.Stop()'''
	'''Motor2.Stop()'''
    
except:
    # GPIO.cleanup()
    print("\nMotor stop") 
    Motor1.Stop()
    '''Motor2.Stop()'''
    exit()
