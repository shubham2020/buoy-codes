import RPi.GPIO as GPIO
import time

class actuator:
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
	
    def __init__(self, freq = 1): # frequePWM
        self.pwm_pin = 40
        GPIO.setup(self.pwm_pin, GPIO.OUT, initial=GPIO.LOW)
        self.freq = freq
        self.pin = GPIO.PWM(self.pwm_pin, self.freq)
        self.dc = 0 #duty cycle
        self.pin.start(self.dc)
        
    def Start(self, dc = 0):
        self.dc = dc
        self.pin.start(self.dc)
        
    def CDC(self, dc ):
        self.dc = dc
        self.pin.ChangeDutyCycle(self.dc)
        
    def Stop(self):
        self.pin.stop()
    
    def CleanUp(self):
        GPIO.cleanup()
        
if __name__=='__main__':
    obj = actuator(100)
    obj.Start()
    obj.CDC(50)
    time.sleep(1000)
    obj.Stop()
        

