import readSensor as rs
import actuation as act
import RPi.GPIO as GPIO
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
    t=0
    while t<300:
        value = sensor.reading()
        t = int(time.time()-t0)
        t_new = str(t//60)+':'+str(t%60)+'   '
        val = str(int(value*10)/10)+'\t\t'+(t_new)+'\r'
        sys.stdout.write(val)
        sys.stdout.flush()
    actuator.Stop()
    GPIO.cleanup()
        

try:
    read()
except KeyboardInterrupt:
    GPIO.cleanup()
