import math
import readSensor as rs
import RPi.GPIO as GPIO
import sys

while True:
	userDecision = input("Enter y to start the bot or q to quit the operation :- ")
	if userDecision == 'y':
		desiredDepth = float(input("Enter the desired depth :- "))
		currentDepth = rs.depth_read()
		Kp =     #Proportional control to be set
		Kd =     #Derivative control to be set
		
		#PWM setup start
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		pwm_pin = 40
		GPIO.setup(pwm_pin, GPIO.OUT, initial=GPIO.LOW)
		freq = 100 				#float(input("Enter the frequency for the system :- "))
		p = GPIO.PWM(pwm_pin, freq) 			
		dutyCycle = 0
		p.start(dutyCycle)				# here number is duty cycle
		#PWM setup over
		
		error = currentDepth - desiredDepth
		error_prev = error
		while math.fabs(currentDepth - desiredDepth)>5:    # Attention:--- this condition for loop exit is to be changed with user decision to change the desired depth
			currentDepth = rs.depth_read()
			error = currentDepth - desiredDepth
			if error < 0:
				p.ChangeDutyCycle(0)
			else:
				error_bar =  error - error_prev
				error_prev = error
				net = Kp*error + Kd*error_bar
				out = 1/(1+math.exp(-net)) - 0.5
				pwm = float(int(out*1000)/10)
				p.ChangeDutyCycle(pwm)
	if userDecision == 'q':
		p.stop() # to stop the heating element 
		sys.exit(0)
	else:
		print ("Choice not recognised ! Please enter a valid choice!!!")
		

			
