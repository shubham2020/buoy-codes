'''
import textFileName as tfn

obj = tfn.date('pwm ')
fname = obj.dateStamp()
print (fname)
'''
'''
import readSensor as rs

obj = rs.sensorRead()
obj.initialization()
for i in range(25):
    print(obj.reading())
'''

import liveMultiPlots as lmp
import threading
obj = lmp.plotLive('one.txt','two.txt')
#obj.action()
t1 =threading.Thread(target = obj.action)
t1.start()

        

