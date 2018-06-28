import math
#import readSensor as rs
import RPi.GPIO as GPIO
import sys
import select
import ms5837
import time

try:
        #Sensor setup start
        sensor = ms5837.MS5837_30BA() 
        # We must initialize the sensor before reading it
        if not sensor.init():
            print "Sensor could not be initialized"
            exit(1)

        # We have to read values from sensor to update pressure and temperature
        if not sensor.read(ms5837.OSR_8192): #reading at 0.2 cm resolution with higher current and read time
            print "Sensor read failed!"
            exit(1)
        time.sleep(5)
        def depth():
            if sensor.read(ms5837.OSR_8192): # reading at 0.2 cm resolution
                    #yield (sensor.depth())
		    return(sensor.depth())
            else:
                    print "Sensor read failed!"
                    exit(1)
            
        #sensor setup complete
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
	while True:
		userDecision = input("Enter 1 to start the bot or 2 to quit :- ")
		if userDecision == 1:
			desiredDepth = float(input("Enter the desired depth :- "))
			currentDepth = depth()
			print (currentDepth)
			Kp = 1    #Proportional control to be set
			Kd = 1    #Derivative control to be set
			
			print ("At any time enter c to change the desired depth or shutdown the bot...")
			error = currentDepth - desiredDepth
			error_prev = error
			while True:
				userChoice = int(input ("To continue with new depth enter 1 and to exit the operation enter 2"))
				if userChoice == 2:
					print("Shutting down the bot !!!")
					p.stop()
					sys.exit(0)
				elif userChoice == 1:
					desiredDepth = float(input("Enter the desired depth :- "))
					while True:    
						
						#code snippet for waiting for any key stroke
						timeout = 0.001
						rlist, wlist, xlist = select.select([sys.stdin], [], [], timeout)
						if rlist:
							break
						#waiting part over
						
						currentDepth = depth()
						error = currentDepth - desiredDepth
						if error < 0:
							p.ChangeDutyCycle(0)
						elif (currentDepth - desiredDepth)>5:
							error_bar =  error - error_prev
							error_prev = error
							net = Kp*error + Kd*error_bar
							out = 1/(1+math.exp(-net)) - 0.5
							pwm = float(int(out*1000)/10)
							p.ChangeDutyCycle(pwm)
				else:
					print("Choice ain't valid. Choose again !!!!")
		if userDecision == 2:
			p.stop() # to stop the heating element 
			sys.exit(0)
		else:
			print ("Choice not recognised ! Please enter a valid choice!!!")
finally:
	p.stop()
	GPIO.cleanup()
		

			
