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
        sensor_obj.initialization()
        print('Now the Ubot is ready to be waterborne')
        
        self.dtname_obj = tfn.dateS('height on ')
        self.pwmname_obj = tfn.dateS('PWM on ')
        self.figname_obj = tfn.dateS('Plot on ')
        self.act_obj = act.actuator() #can pass frequency as an argument
        self.plt_obj = 0
        
        self.dtname = ''
        self.pwmname = ''
        self.figname = ''
        
        self.Kp = 0
        self.Kd = 0
        self.Ki = 0
        
        self.desired_depth = 0
        self.current_depth = 0
        self.pwm = 0
        self.t = 0
        self.dt = 0
        # both the flags should be zero for operation
        self.shutflag = 0
        self.writeflag = 0
        
        
    def initialize(self): #initialize by preparing file names
        self.htname_obj.forText()
        self.pwmname_obj.forText()
        self.figname_obj.forFig()
        self.dtname = self.dtname_obj.dateStamp()
        self.pwmname = self.pwmname_obj.dateStamp()
        self.figname = self.figname_obj.dateStamp()
        self.plt_obj = lmp.plotLive(self.dtname,self.pwmname,self.figname, self.Kp, self.Kd, self.Ki)
        #now call self.plt_obj.action when required the live plotting
        
    def user_depth_input(self): #thread 1
        while True:
            user_input = input('Enter the new desired depth or e to exit : ')
            if user_input.lower() == 'e':
                self.shutflag = 1
                self.writeflag = 1
                return
            else:
                self.desired_depth = float(user_input)
    
    def writing_text(self): #thread 2
        #including display part by writing it to a file
	#self.t = self.t+self.dt
        while True:
            if self.writeflag == 0:
                msg1 = str(int(self.t/1000))+','+str(self.current_depth)+'\n'
                msg2 = str(int(self.t/1000))+','+str(self.pwm)+'\n'
                with open(self.dtname,'a') as file1:
                    file1.write(msg1)
                with open(self.pwmname,'a') as file2:
                    file2.write(msg2)
                #print('{0:10}{1}'.format(self.current_depth, self.pwm))
            elif self.writeflag == 1:
                return
	
    def plot_data(self): #thread 3
        self.plt_obj.action()
        self.shutflag = 1
        self.writeflag = 1
						
						
    def controller(self): #thread 4
        e1 = time.time() # for computing dt first time
        error_int = 0
        self.act_obj.Start(0)
        while True:
            if self.shutflag == 0:
                self.current_depth = self.sensor_obj.reading()
                error = (self.current_depth - self.desired_depth)
                if math.fabs(error) < 0.4: #to stop actuation once we reach within +/-2cm of target depth
                    print("Bot within no action range")
                    self.act_obj.CDC(0) #to stop actuation which otherwise continues with previous values
                    continue
                e2 = time.time() #time ends now
                self.dt = (int((e2 - e1)*1000))
                e1 = time.time() #time starts now
                error_bar =  ((error - error_prev)*1000)/self.dt
                error_prev = error
                error_int = error_int + error*(self.dt/1000)
                net = self.Kp*error + self.Kd*error_bar + self.Ki*error_int
                out = (1/(1+math.exp(-net)))  #sigmoid function to bound pwm
                pwm = float(int(out*1000)/10)
                self.act_obj.CDC(pwm) #changing duty cycle
                self.t = self.t+self.dt
                
            elif self.shutflag == 1:
                self.act_obj.Stop()
                return
        
        
        
if __name__='__main__':
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
    while True:
        obj.desired_depth = float(input('Enter the desired depth :- '))
        thread4.start()  #starting the controller
        thread2.start()  #starting the text writting
        thread3.start()  #starting the live plotting
        thread1.start()  #starting the user prompt
        
        thread4.join()   #as user hits e thread1 stops, thread2 stops, thread4 stops
                         #thread3 is user dependent as user closes the window the graph gets saved and
                         #thread gets stopped
                         #also if user closes graph window thread4, thread2 , thread3 get stopped and
                         #thread1 being daemon thread gets killed as the main exits
        print('This exit means Ubot has to be taken out of water for next usage')
        n = input('Enter e to exit and n to continue operation :- ')
        if n.lower() == 'e':
            obj.act_obj.CleanUp()
            print('Ubot has been shut down!!!')
            break
        else
            obj.initialize() #to create new text files and new graphs from fresh
            continue
        
    
        


