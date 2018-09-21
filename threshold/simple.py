import readSensor as rs
import actuation as act
import threading
import sys
import time

sensor = rs.sensorRead()
actuator = act.actuator()
sensor.initialization()
pwm = 0
def read():
    pwm = float(input('Enter PWM value :-'))
    actuator.CDC(pwm)
    t0 = time.time()
    print('Depth(cm)\tTime')
    while True:
        value = sensor.reading()
        t = int(time.time()-t0)
        t_new = str(t//60)+':'+str(t%60)
        value = str(int(value*10)/10)+'\t\t'+t_new+'\r'
        sys.stdout.write(value)
        sys.stdout.flush()        
        
if __name__ == '__main__':
    read()
