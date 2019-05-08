import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

while 1: 
    if(ser.in_waiting >0):		#to check if the buffer has some data (its type is int)
        hexa = ser.readline()
        print(hexa)
        #if len(hexa)>0:
        line = (float(int(ser.readline(),16)))/10
        #line = ser.readline()
        #if line < 5:
        #    print(line)
        #pieces = line.split(" ")
        #print(pieces)
        #if len(pieces[0])>0:
        #    value = float(pieces[0])
        #    print(value)
        #time.sleep(1)
