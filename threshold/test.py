'''
import textFileName as tfn

obj = tfn.date('pwm ')
obj.forText()
fname = obj.dateStamp()
obj.forFig()
figName = obj.dateStamp()
print (figName)
print (fname)
'''
'''
import readSensor as rs

obj = rs.sensorRead()
obj.initialization()
for i in range(25):
    print(obj.reading())
'''
'''
import liveMultiPlots as lmp
import threading

obj = lmp.plotLive('one.txt','two.txt','three.jpg')
        
t1 = threading.Thread(target = obj.action)
#t1.daemon =True
t1.start()
print("main thread ended")
'''

import actuation as act
import time

obj = act.actuator()
obj.Start(0)
time.sleep(1)
obj.CDC(0)
time.sleep(1)
obj.Stop()
obj.CleanUp()

'''
import time

print('I am going to sleep!')
time.sleep(0.25)
print('I woke up!')
'''