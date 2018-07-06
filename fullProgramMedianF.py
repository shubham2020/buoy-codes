import math
#import readSensor as rs
import RPi.GPIO as GPIO
import sys
import select
import ms5837
import time

try:    # Global variables
        i = 0 #for graph plotting purposes
        # Global variables end
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
        sensor.read(ms5837.OSR_8192)
        calib_depth = sensor.depth()*100
        n = 51 #sensor window size for median or mean filter
        arr = [0]*n
	''' #this is implementation of mean filter
        def depth():
            if sensor.read(ms5837.OSR_8192): # reading at 0.2 cm resolution
                for j in range(n-1):         # moving average calculation starts here
                    arr[j]=arr[j+1]
                arr[j+1]=sensor.depth()*100 - calib_depth   #removing calibration offset in environment
                avg_sensor_reading = sum(arr)/n  #moving average calculation ends here
                return(avg_sensor_reading) 
            else:
                print "Sensor read failed!"
                exit(1)'''
				
	def depth(): #this is implementation of median filter
            if sensor.read(ms5837.OSR_8192): # reading at 0.2 cm resolution
                for j in range(n):         
                    arr[j]=sensor.depth()*100 - calib_depth
		temp = arr[0]
                for i in range(n-1):
		    for j in range(i,n):
			if arr[i]>arr[j]:
			    temp = arr[i]
			    arr[i] = arr[j]
			    arr[j] = temp
		median_depth = arr[(int(n/2)+1)]
                return(median_depth) 
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
	p.start(dutyCycle)# here number is duty cycle
	pwm = 0
	#PWM setup over
	while True:
		userDecision = input("Enter 1 to start the bot or 2 to quit :- ")
		if userDecision == 1:
			desiredDepth = float(input("Enter the desired depth :- "))
			currentDepth = depth()
			print (currentDepth)
			Kp = .5    #Proportional control to be set
			Kd = .07    #Derivative control to be set
			Ki = 0    #Integral control to be set
			
			print ("At any time enter 1 to continue with new depth or enter 2 to Shutdown the bot....")
			error = (currentDepth - desiredDepth)
			error_prev = error
			while True:
                                error_int = 0
				userChoice = int(input ())
				if userChoice == 2:
					print("Shutting down the bot !!!")
					p.stop()
					sys.exit(0)
				elif userChoice == 1:
					desiredDepth = float(input("Enter the desired depth :- "))
                                        e1 = time.time() #this is for first time calculation
                                        while True:    
						#code snippet for waiting for any key stroke
						timeout = 0.001
						rlist, wlist, xlist = select.select([sys.stdin], [], [], timeout)
						if rlist:
							break
						#waiting part over
						
						currentDepth = depth()
						error = (currentDepth - desiredDepth)
						if math.fabs(error) < 0.4: #to stop actuation once we reach within +/-2cm of target depth
                                                    print("Bot within no action range")
                                                    p.ChangeDutyCycle(0) #to stop actuation which otherwise continues with previous values
                                                    continue
                                                e2 = time.time() #time ends now
                                                dt = (int((e2 - e1)*1000))
						error_bar =  ((error - error_prev)*1000)/dt
						error_prev = error
						error_int = error_int + error*dt
						e1 = time.time() #time starts now
						net = Kp*error + Kd*error_bar + Ki*error_int
						out = (1/(1+math.exp(-net)))  #sigmoid function to bound pwm
						pwm = float(int(out*1000)/10)
						p.ChangeDutyCycle(pwm)
						'''
						if error < 0:
                                                        pwm = 0
							p.ChangeDutyCycle(pwm)
						elif (currentDepth - desiredDepth)>5:
							error_bar =  error - error_prev
							error_prev = error
							net = Kp*error + Kd*error_bar
							out = (1/(1+math.exp(-net)))
							pwm = float(int(out*1000)/10)
							p.ChangeDutyCycle(pwm)
						'''
						#including display part by writing it to a file
						i = i+dt
						msg1 = str(i)+','+str(error)+'\n'
						msg2 = str(i)+','+str(pwm)+'\n'
						with open('/home/pi/buoy-codes/data files/errorData1(5July18).txt','a') as file1:
                                                    file1.write(msg1)
                                                with open('/home/pi/buoy-codes/data files/pwmData1(5July18).txt','a') as file2:
                                                    file2.write(msg2)
						print(str(error)+'\t\t'+str(pwm))
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
		

			
