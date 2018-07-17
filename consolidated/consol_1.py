#standard or other libraries
import math
import time
import threading
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
        
        #self.htname_obj.forText()
        #self.pwmname_obj.forText()
        #self.figname_obj.forFig()
        
        self.ddname = ''
        self.dtname = ''  #the returned names will be stored in these variables
        self.pwmname = ''
        self.figname = ''
        
        self.Kp = 0.005
        self.Kd = 0.001
        self.Ki = 0
        
        self.desired_depth = 0
        self.current_depth = 0
        self.pwm = 0
        self.t = 0
        self.dt = 0
        # both the flags should be zero for operation
        self.shutflag = 0
        self.writeflag = 0
        
        #self.input_lock = threading.Lock() # to prevent multiple promts as in depth and exiting
        
        
    def initialize(self): #initialize by preparing file names
        ddname_obj = tfn.dateS('des. depth on ')
        dtname_obj = tfn.dateS('curr depth on ')
        pwmname_obj = tfn.dateS('PWM on ')
        figname_obj = tfn.dateS('Plot on ')
        ddname_obj.forText()
        dtname_obj.forText()
        pwmname_obj.forText()
        figname_obj.forFig()
        self.ddname = ddname_obj.dateStamp()
        self.dtname = dtname_obj.dateStamp()
        self.pwmname = pwmname_obj.dateStamp()
        self.figname = figname_obj.dateStamp()
        self.plt_obj = lmp.plotLive(self.ddname,self.dtname,self.pwmname,self.figname, self.Kp, self.Kd, self.Ki)
        #now call self.plt_obj.action when required the live plotting
        
    def user_depth_input(self): #thread 1
        while True:
            #with self.input_lock: #to prevent multiple prompts at a time
            user_input = float(input('Enter the new desired depth or 1 to exit :- '))
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
        while True:
            if self.writeflag == 0:
                #with self.plt_obj.rw_lock:
                    msg0 = str(int(self.t/1000))+','+str(self.desired_depth)+'\n'
                    msg1 = str(int(self.t/1000))+','+str(float(int((self.current_depth)*10)/10))+'\n'
                    msg2 = str(int(self.t/1000))+','+str(self.pwm)+'\n'
                    #with open(self.ddname,'a')as file0:
                    file0.write(msg0)
                    #with open(self.dtname,'a') as file1:
                    file1.write(msg1)
                    #with open(self.pwmname,'a') as file2:
                    file2.write(msg2)
                    time.sleep(0.1) #put values in decimals not division manner
                    #print('{0}\t\t\t{1}'.format(self.current_depth, self.pwm))
            elif self.writeflag == 1:
                file0.close()
                file1.close()
                file2.close()
                return
	
    def plot_data(self): #thread 3
        self.plt_obj.action()  #its object has been created in the initialize
        self.shutflag = 1
        self.writeflag = 1
						
						
    def controller(self): #thread 4
        e1 = time.time() # for computing dt first time
        error_int = 0
        self.act_obj.Start(0)
        error_prev = 0
        while True:
            if self.shutflag == 0:
                self.current_depth = self.sensor_obj.reading()
                error = (self.current_depth - self.desired_depth)
                e2 = time.time() #time ends now
                self.dt = (int((e2 - e1)*1000))
                e1 = time.time()
                self.t = self.t+self.dt
                if math.fabs(error) < 0.4 or error < 0: #to stop actuation once we reach within +/-2cm of target depth
                    #print("Bot within no action range")
                    self.pwm = 0
                    self.act_obj.CDC(self.pwm) #to stop actuation which otherwise continues with previous values
                    continue
                #e2 = time.time() #time ends now
                #self.dt = (int((e2 - e1)*1000))
                #e1 = time.time() #time starts now
                error_bar =  ((error - error_prev)*1000)/self.dt
                error_prev = error
                error_int = error_int + error*(self.dt/1000)
                net = self.Kp*error + self.Kd*error_bar + self.Ki*error_int
                out = (1/(1+math.exp(-net)))  #sigmoid function to bound pwm
                self.pwm = float(int(out*1000)/10)
                self.act_obj.CDC(self.pwm) #changing duty cycle
                #self.t = self.t+self.dt
                
                #self.writing_text()
                
            elif self.shutflag == 1:
                self.act_obj.Stop()
                return
        
        
        
if __name__=='__main__':
    obj = Ubot()
    obj.initialize()
    thread1 = threading.Thread(target = obj.user_depth_input)
    thread2 = threading.Thread(target = obj.writing_text)
    thread3 = threading.Thread(target = obj.plot_data) #we had a plot saving issue
    thread4 = threading.Thread(target = obj.controller)
    thread1.daemon = True
    thread2.daemon = True
#    thread3.daemon = True
    thread4.daemon = True
    #while True:
    obj.desired_depth = float(input('Enter the desired depth :- '))
    thread4.start()  #starting the controller
    thread2.start()  #starting the text writting
    thread3.start()  #starting the live plotting
    thread1.start()  #starting the user prompt
        
    thread4.join()       #as user hits 'e' thread1 stops, thread2 stops, thread4 stops
                         #thread3 is user dependent as user closes the window the graph gets saved and
                         #thread gets stopped
                         #also if user closes graph window thread4, thread2 , thread3 get stopped and
                         #thread1 being daemon thread gets killed as the main exits
    #with obj.input_lock:    #trying this to stop multiple prompts as in depth and here
        #print('Caution : This exit means Ubot has to be taken out of water for next usage')
        #n = int(input('Enter 1 to exit and 2 to continue operation :- '))
    #if n == 1:
    #thread3.start()
    obj.act_obj.CleanUp()
    print('Ubot has been shut down!!!')
        #break
    #else:
        #obj.initialize() #to create new text files and new graphs from fresh
        #continue
    
        


