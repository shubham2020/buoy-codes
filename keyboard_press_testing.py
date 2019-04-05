
import time
import keyboard
import sys

pwm = 0

while True:
            if keyboard.is_pressed('u') and pwm < 100:
                print(pwm)
                pwm = pwm +1
                time.sleep(0.08)
                continue
            if keyboard.is_pressed('j') and pwm > 0:
                print(pwm)
                pwm = pwm -1
                time.sleep(0.08)
                continue
            if keyboard.is_pressed('e'):
                #self.shutflag = 1
                #self.writeflag = 1
                sys.exit
            else:
                print(pwm)
                pass
