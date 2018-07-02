#!/usr/bin/python
import ms5837
import time

def depth_read():
    sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)
    #sensor = ms5837.MS5837_30BA(0) # Specify I2C bus
    #sensor = ms5837.MS5837_02BA()
    #sensor = ms5837.MS5837_02BA(0)
    #sensor = ms5837.MS5837(model=ms5837.MS5837_MODEL_30BA, bus=0) # Specify model and bus

    # We must initialize the sensor before reading it
    if not sensor.init():
            print "Sensor could not be initialized"
            exit(1)

    # We have to read values from sensor to update pressure and temperature
    if not sensor.read(ms5837.OSR_8192): #read at .2 cm resolutin with high current and large read time
        print "Sensor read failed!"
        exit(1)
    '''
    print("Pressure: %.2f atm  %.2f Torr  %.2f psi") % (
    sensor.pressure(ms5837.UNITS_atm),
    sensor.pressure(ms5837.UNITS_Torr),
    sensor.pressure(ms5837.UNITS_psi))

    print("Temperature: %.2f C  %.2f F  %.2f K") % (
    sensor.temperature(ms5837.UNITS_Centigrade),
    sensor.temperature(ms5837.UNITS_Farenheit),
    sensor.temperature(ms5837.UNITS_Kelvin))
    '''
    #freshwaterDepth = sensor.depth() # default is freshwater
    #sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
    #saltwaterDepth = sensor.depth() # No nead to read() again
    #sensor.setFluidDensity(1000) # kg/m^3
    #print("Depth: %.3f m (freshwater)  %.3f m (saltwater)") % (freshwaterDepth, saltwaterDepth)

    # fluidDensity doesn't matter for altitude() (always MSL air density)
    #print("MSL Relative Altitude: %.2f m") % sensor.altitude() # relative to Mean Sea Level pressure in air

    time.sleep(5)
    i=0
    t=0
    # Spew readings
    while True:
            if sensor.read(ms5837.OSR_8192):
                    if i == 20 or i == 0:
                        print("Depth(in cm) \t \t Pressure(in mbar) \t \t Temperature(in deg C)")
                        i = 0
                    '''
                    print("P: %0.1f mbar  %0.3f psi\tT: %0.2f C  %0.2f F") % (
                    sensor.pressure(), # Default is mbar (no arguments)
                    sensor.pressure(ms5837.UNITS_psi), # Request psi
                    sensor.temperature(), # Default is degrees C (no arguments)
                    sensor.temperature(ms5837.UNITS_Farenheit)) # Request Farenheit
                    '''
                    depth1 = sensor.depth()*100
                    depth2 = sensor.pressure()
                    print("{} \t \t {} \t \t \t \t {}".format(depth1,depth2,sensor.temperature()))
                    i=i+1
                    t=t+1
                    msg = str(t)+','+str(depth1)+'\n'
                    with open("testData.txt","a") as f:
                        f.write(msg)
                    time.sleep(1)
            else:
                    print "Sensor read failed!"
                    exit(1)
if __name__ == "__main__":
    depth_read()