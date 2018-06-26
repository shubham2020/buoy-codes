import RPi.GPIO as GPIO


def runPWM():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    pwm_pin = 8
    GPIO.setup(pwm_pin, GPIO.OUT, initial=GPIO.LOW)
    freq = float(input("Enter the frequency for the system :- "))
    dc = int(input("Enter the duty cycle to begin with :- "))
    p = GPIO.PWM(pwm_pin, freq)#  is the frequency
    p.start(dc)#here number is duty cycle
    k=0
    e='e'
    q='q'
    try:
        while True:
            k = str(input("Enter e to reset Duty Cycle or q to quit the operation :- "))
            if k == e:
                p.stop()
                dc = float(input("Enter duty cycle in percentage :- "))
                p = GPIO.PWM(pwm_pin, freq)
                p.start(dc)
            elif k == q:
                break
    finally:
        p.stop()
        GPIO.cleanup()#return all channels we have used in this script back to inputs with no pull up/down
if __name__=="__main__":
    runPWM()