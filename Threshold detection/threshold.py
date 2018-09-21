import readSensor as rs
import actuation as act
import textFileName as tfn
import liveMultiPlots as lp
import threading
import multiprocessing
import time
import sys

class thresholds:
    def __init__(self):
        self.sensor = rs.sensorRead()
        self.actuator = act.actuator()
        self.names = tfn.dateS('threshold tests ')
        self.pwm = 0
        self.fname = None
        self.plot = None
        self.shutflag = 0 #for killing the thread as soon as the task is done
        
    def initialization(self):
        self.sensor.initialization()
        self.fname = self.names.dateStamp()
        self.plot = lp.plotLive(self.fname, self.names.dateStamp(1),self.pwm)
            
    def readWrite(self):
        t1 =  time.time()
        file = open(self.fname,'a')
        t = 0
        while self.shutflag == 0:   
            value = self.sensor.reading()
            t2 = time.time()
            dt = (float(int((t2-t1)*1000)))/1000
            t1 = time.time()
            t = t + dt
            file.write(str(t)+','+str(value)+'\n')
            time.sleep(.1)
            
        file.close()
    
    def plotting(self):
        self.plot.action()
        self.shutflag = 1
    
    def UserEnter(self):
        while self.shutflag == 0:
            self.pwm = float(input('Enter the pwm value :- '))
            self.actuator.CDC(self.pwm)
            t0 = time.time()
            while (time.time()-t0)<300:
                t = int((300 - (time.time()-t0)))
                msg = str(t//60)+':'+str(t%60)+'\r'
                sys.stdout.write(msg)
                sys.stdout.flush()
                time.sleep(1)
        self.actuator.Stop()
        
    #def readingSensor(self):
    #    depth = self.sensor.reading()
        
if __name__ == '__main__':
    object = thresholds()
    object.initialization()
    thread1 = threading.Thread(target = object.UserEnter)
    thread2 = threading.Thread(target = object.readWrite)
    #process = multiprocessing.Process(target = object.plotting)
    thread2.start()
    thread1.start()
    #process.start()
    object.actuator.CleanUp()
    
    
    
        