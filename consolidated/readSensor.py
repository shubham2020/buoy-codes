#!/usr/bin/python
import ms5837
import time

class sensorRead:
    def __init__(self, n = 51):
        self.sensor = ms5837.MS5837_30BA()
        self.n = n #window size for median filter
        self.calib_depth = 0        

    def initialization(self):
        # We must initialize the sensor before reading it
        if not self.sensor.init():
            print "Sensor could not be initialized"
            exit(1)

        # We have to read values from sensor to update pressure and temperature
        if not self.sensor.read(ms5837.OSR_8192): #reading at 0.2 cm resolution with higher current and read time
            print "Sensor read failed!"
            exit(1)
        
        time.sleep(5)
        self.sensor.read(ms5837.OSR_8192)
        self.calib_depth = self.sensor.depth()*100  
    
    # Spew readings
    def reading(self):
            arr = [0]*self.n
            if self.sensor.read(ms5837.OSR_8192): # reading at 0.2 cm resolution
                for j in range(self.n):         # median filter applied
                    arr[j]=self.sensor.depth()*100 - self.calib_depth
		temp = arr[0]
                for i in range(self.n-1):
		    for j in range(i,self.n):
			if arr[i]>arr[j]:
			    temp = arr[i]
			    arr[i] = arr[j]
			    arr[j] = temp
		median_depth = arr[(int(self.n/2)+1)]
		#print (median_depth)
                return(median_depth)
			
            else:
                print "Sensor read failed!"
                exit(1)
if __name__ == "__main__":
    s = sensorRead()
    s.initialization()
    s.reading()
