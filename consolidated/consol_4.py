# removed user depth input's while loop, by adding the while loop we can indefinitely give desired depth


#standard or other libraries
import math
import time
import threading
import multiprocessing
import sys
#user defined classes and functions
import textFileName as tfn
import readSensor as rs
import liveMultiPlots as lmp
import actuation as act

class Ubot:
    
    def __init__(self): #initialize sensor for calib_depth and create objects of classes
        
        print('Keep the Ubot out of water')
        self.sensor_obj = rs.sensorRead() #can pass filter window size as an argument
        self.sensor_obj.initialization()
        print('Now the Ubot is ready to be waterborne')
        
        #self.dtname_obj = tfn.dateS('height on ')
        #self.pwmname_obj = tfn.dateS('PWM on ')
        #self.figname_obj = tfn.dateS('Plot on ')
        self.act_obj = act.actuator() #can pass frequency as an argument
        self.plt_obj = None
        
        #self.dtname_obj.forText()
        #self.pwmname_obj.forText()
        #self.figname_obj.forFig()
        
        self.ddname = ''  #desired depth
        self.dtname = ''  #the returned names will be stored in these variables
        self.pwmname = ''
        self.figname = ''
        self.velname = ''
        
        self.Kp = 0.05
        self.Kd = 0.05
        self.Ki = 0
        
        self.desired_depth = 0
        self.current_depth = 0
        self.pwm = 0
        self.t = 0
        self.dt = 0
        self.velocity = 0
        
        # both the flags should be zero for operation
        
        self.shutflag = 0
        self.writeflag = 0
        
        #self.threshold = 2.1972 #for making the bot neutrally buoyant i.e. at any depth it can hover
        
        #Experimentally determined values of PWM and corresponding power values 
        self.power = [0, 3.6, 7.68, 10.92, 15.64, 19.19, 23.31, 27.14, 32, 34.58, 37.8]
        self.pulse = [0, 32.1, 45.7, 55.7, 65.7, 72.1, 79.3, 84.3, 91.4, 95, 100]
        
        #self.input_lock = threading.Lock() # to prevent multiple promts as in depth and exiting
        
        #####################################
        # for adding relay in the circuit
        self.relay_pin = 36
        GPIO.setup(self.relay_pin, GPIO.OUT, initial=GPIO.LOW)
        #####################################
        
        
    def initialize(self): #initialize by preparing file names
        ddname_obj = tfn.dateS('des. depth on ') #objects for the imported user modules are created and initialized
        dtname_obj = tfn.dateS('curr depth on ')
        pwmname_obj = tfn.dateS('PWM on ')
        figname_obj = tfn.dateS('Plot on ')
        velocity_obj = tfn.dateS('Velocity on ')
        ddname_obj.forText()
        dtname_obj.forText()
        pwmname_obj.forText()
        figname_obj.forFig()
        velocity_obj.forText()
        self.ddname = ddname_obj.dateStamp()
        self.dtname = dtname_obj.dateStamp()
        self.pwmname = pwmname_obj.dateStamp()
        self.figname = figname_obj.dateStamp()
        self.velname = velocity_obj.dateStamp()
        self.plt_obj = lmp.plotLive(self.ddname,self.dtname,self.pwmname,self.figname, self.Kp, self.Kd, self.Ki, 500)
        #now call self.plt_obj.action when required the live plotting
        
    def user_depth_input(self): #thread 1
        #while True:
            #with self.input_lock: #to prevent multiple prompts at a time
            user_input = float(input("Enter the kill code :-"))#'Enter the new desired depth or 1 to exit :- '))
            if user_input == 1:
                self.shutflag = 1
                self.writeflag = 1
                return
            else:
                self.desired_depth = float(user_input)
    
    def writing_text(self): #thread 2
        #including display part by writing it to a file
	#self.t = self.t+self.dt
        #t = self.t # to ensure all are saving the same time for the parallel graph plotting
        file0 = open(self.ddname,'a')
        file1 = open(self.dtname,'a')
        file2 = open(self.pwmname,'a')
        file3 = open(self.velname,'a')
        while True:
            #correct these file writtings using the consol_1.py method
            if self.writeflag == 0:
                msg0 = str(int(self.t/1000))+','+str(self.desired_depth)+'\n'
                msg1 = str(int(self.t/1000))+','+str(int(self.current_depth*10)/10)+'\n'
                msg2 = str(int(self.t/1000))+','+str(self.pwm)+'\n'
                msg3 = str(int(self.t/1000))+','+str(int(self.velocity*10)/10)+'\n'
                file0.write(msg0)
                file1.write(msg1)
                file2.write(msg2)
                file3.write(msg3)
                time.sleep(0.1)
                #print('{0:10}{1}'.format(self.current_depth, self.pwm))
            elif self.writeflag == 1:
                file0.close()
                file1.close()
                file2.close()
                file3.close()
                return
	
    def plot_data(self): # process 3 rather than thread 3
        self.plt_obj.action()  #its object has been created in the initialize
        self.shutflag = 1
        self.writeflag = 1
        
    def screenWrite(self): # thread 5
        #print('\nerror\tPWM\tCurrent Depth\tVelocity')
        print('\nerror\tPWM\tCurrent Depth\tVelocity\tTime')
        # this part is for timing the code
        t0 = time.time()
        t=0
        #while self.shutflag == 0:
        while self.shutflag == 0:
            # call user_depth_input when needed else print error pwm current depth and
            # desired depth live
            # So ask for user interrupt for entering desired depth
            ############################ timing part for open loop tests
            t = int(time.time()-t0)
            t_new = str(t//60)+':'+str(t%60)+'   '
            ############################
            error = int(self.current_depth*10)/10 - self.desired_depth
            msg = str(error)+'\t'+str(self.pwm)+'\t'+str(int(self.current_depth*10)/10)+'\t\t'+str(int(self.velocity*10)/10)+'\t\t'+t_new+'\r'            
            sys.stdout.write(msg)
            sys.stdout.flush()
            time.sleep(0.01)
        else:
            #self.shutflag = 1 # this part added for open loop test
            return
    
    def interpolate(self,p):
        for i in range(len(self.power)):
            if (p >= self.power[i]) and (p <= 37.8):
                out = ((self.pulse[i+1]-self.pulse[i])/(self.power[i+1]-self.power[i]))*(p-self.power[i])+self.pulse[i]
		#print(out)
		return out
	    if (p > 37.8):
                return (100.0) # this condition will take care for any negative values
            else:
                return (0)
						
    def controller(self): #thread 4
        e1 = time.time() # for computing dt first time
        #error_int = 0
        self.act_obj.Start(0)
        error_prev = self.desired_depth
        v1 = self.sensor_obj.reading()
        p0 = 0 #value for apparant weight divide by a constant i.e. power required for neutral buoyancy
        self.Kp = 0.05 #declared here again so as not to go to initializations again and again
        self.Kd = 0.05
        while True:
            if self.shutflag == 0:
                ###############relay pin control ##################
                GPIO.output(self.relay_pin, HIGH)
                ###################################################
                self.current_depth = self.sensor_obj.reading()
                # To rectify error i am simulating error to be 40
                error = (self.current_depth - self.desired_depth)
                e2 = time.time() #time ends now
                self.dt = (int((e2 - e1)*1000))
                e1 = time.time() #time starts now
                self.t = self.t + self.dt
                # code for velocity calculation using rate of depth change
                v2 = self.sensor_obj.reading()
                self.velocity = (v2 - v1)/self.dt
                v1 = self.sensor_obj.reading()
                #error = error if error >= 0 else 0 # to reject negative errors as they mean actuate when desired depth is below the current depth
                #error_bar =  ((error - error_prev)*1000)/self.dt
                error_bar =  ((self.current_depth - error_prev)*1000)/self.dt
                error_prev = self.current_depth
                #error_prev = error
                #error_int = error_int + error*(self.dt/1000)
                p = p0 + self.Kp*error + self.Kd*error_bar #+ self.Ki*error_int
                #print(p)
                out = self.interpolate(p)#(1/(1+math.exp(-net+self.threshold)))#sigmoid function to bound pwm
                #print(out)
                self.pwm = float(int(out*10))/10 # this will truncate any values after 1 decimal place
                self.act_obj.CDC(self.pwm) #changing duty cycle
                time.sleep(0.5) # reduced the actuation frequency
                                
            elif self.shutflag == 1:
                GPIO.output(self.relay_pin,LOW) #relay pin control
                self.act_obj.Stop()
                return
        
        
        
if __name__=='__main__':
    obj = Ubot()
    obj.initialize()
    thread1 = threading.Thread(target = obj.user_depth_input)
    thread2 = threading.Thread(target = obj.writing_text)
    #thread3 = threading.Thread(target = obj.plot_data) #we had a plot saving issue
    #process = multiprocessing.Process(target = obj.plot_data) #here using only one extra process for plotting rest can be assimilated in threading
    thread4 = threading.Thread(target = obj.controller)
    thread5 = threading.Thread(target = obj.screenWrite)
    #thread1.daemon = True
    thread2.daemon = True
    #thread3.daemon = True
    thread4.daemon = True
    thread5.daemon = True
    obj.desired_depth = float(input('Enter the desired depth :- '))
    thread4.start()  #starting the controller
    thread2.start()  #starting the text writting
    #thread3.start()  #starting the live plotting
    #process.start()   #starting the live plotting process
    thread1.start()  #starting the user prompt
    thread5.start()  #for screen write
        
    thread1.join()
    obj.plot_data()        #as user hits 'e' thread1 stops, thread2 stops, thread4 stops
    obj.act_obj.CleanUp()
    print('Ubot has been shut down!!!')

    
        


