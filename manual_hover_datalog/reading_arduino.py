import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

while 1: 
    if(ser.in_waiting >0):		#to check if the buffer has some data (its type is int)
        line = ser.readline()
        print(line)
