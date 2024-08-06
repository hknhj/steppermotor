import RPi.GPIO as GPIO
import time
import threading
from DRV8825 import DRV8825

switch_UNDER = GPIO.LOW
switch_UPPER = GPIO.LOW
cur_x = 0 #
cur_y = 0 #

def initLocation(motor):
	print('initializing motor...')
	
	switch_thread1 = threading.Thread(target=monitor_switch, args=(14,))
	switch_thread2 = threading.Thread(target=monitor_switch, args=(15,))
	motor_thread1 = threading.Thread(target=toEndUnder, args=(1,0))
	motor_thread2 = threading.Thread(target=toEndUpper, args=(2,0))
	
	switch_thread1.start()
	switch_thread2.start()
	motor_thread1.start()
	motor_thread2.start()
	

def monitor_switch(switch_num):
	global switch_UNDER
	global switch_UPPER

	while True:
		switch_state = GPIO.input(switch_num)
		if switch_state == GPIO.HIGH:
			if switch_num == 14:
				switch_UNDER = GPIO.HIGH
			else:
				switch_UPPER = GPIO.HIGH
			print(f'switch {switch_num} pressed')
			break
		else:
			print(f'switch {switch_num} NOT pressed')
		time.sleep(0.1)

def toEndUnder(motor_num, direction):
	while switch_UNDER == GPIO.LOW:
		moveMotor(motor_num, direction)
		
def toEndUpper(motor_num, direction):
	while switch_UPPER == GPIO.LOW:
		moveMotor(motor_num, direction)

def moveMotor(motor_num, direction):
	# 0: toward the motor, 1: far away from the motor
	motor = Motor1 if motor_num == 1 else Motor2
	
	motor.digital_write(motor.enable_pin, 1)
	motor.digital_write(motor.dir_pin, direction)
	motor.digital_write(motor.step_pin, True)
	time.sleep(0.001)
	motor.digital_write(motor.step_pin, False)
	time.sleep(0.001)
	
def scan():
	global Motor1
	global Motor2
	
	x,y = map(int, input('enter x,y: ').split())
	steps = 300
	
	motor1_thread = threading.Thread(target=moveMotor, args=(1,0))
	motor2_thread = threading.Thread(target=moveMotor, args=(2,0))
		
	return location

def doingJob(motor):
	motor.TurnStep(Dir='forward', steps=1600, stepdelay=0.001)
	time.sleep(0.5)
	motor.TurnStep(Dir='backward', steps=1600, stepdelay=0.001)
	motor.Stop()
	
def motorTest():
	thread1 = threading.Thread(target=doingJob, args=(Motor1,))
	thread2 = threading.Thread(target=doingJob, args=(Motor2,))
	
	thread1.start()
	thread2.start()
	

# init stppermotor
Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
Motor1.SetMicroStep('softward' ,'1/8step')    
Motor2.SetMicroStep('softward' ,'1/8step')  

# init GPIO with pull down resistance
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


try:
	# init motor location
	initLocation(Motor1)
	
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

	'''
	Motor1.TurnStep(Dir='forward', steps=200, stepdelay=0.001)
	time.sleep(0.5)
	Motor1.TurnStep(Dir='backward', steps=200, stepdelay=0.001)
	Motor1.Stop()
	'''

	'''Motor1.Stop()'''
	'''Motor2.Stop()'''
    
except:
    print("\nMotor stop") 
    exit()
