#############	System libraries	#################
import serial
import xlsxwriter
import time
import sys
#############		End				#################

#############	User defined libraries	#############
import textFileName as tfn
import readSensor as rs
#############			End				#############

class datalog:
	def __init__(self):
		self.sensor_obj = rs.sensorRead() #can pass filter window size as an argument
                self.sensor_obj.initialization()
                print('Sensor initalized and calibrated')
                file_name_object = tfn.dateS(sys.argv[1]+' hovering data_log on ')      #to sync the name of the video and the experiment
                file_name_object.forText()
                file_name = file_name_object.dateStamp()
                self.workbook = xlsxwriter.Workbook(file_name)
                self.worksheet = self.workbook.add_worksheet()
        
                self.worksheet.write(0,0,'Time(s)')
                self.worksheet.write(0,1,'Voltage(V)')
                self.worksheet.write(0,2,'Depth(cm)')
                self.worksheet.write(0,3,'Current(A)')
        
                self.current_depth = 0
                self.line = 0

                self.ser = serial.Serial('/dev/ttyACM0', 9600)		#object for getting handle of serial communication
        
        def logging(self):
		row = 1
		t1 = time.time()
		t2 = time.time()
		while True:
			self.current_depth = self.sensor_obj.reading()
			self.current_depth = int(self.current_depth*10)/10
			if (self.ser.in_waiting >0) and len(self.ser.readline()) > 0:		# to check if the buffer has some data (its type is int)
                                try:
                                        self.line = (float(int(self.ser.readline(),16)))/10
                                        #self.line = self.ser.readline()
                                        print(self.line)
                                except ValueError:
                                        print("Value Error occured!!!")
                                        continue
			else:
				continue
			for col in range(0,4):
				if col == 0:
                                        t2 = time.time()
					#print(t2)
					item = (float(int((t2 - t1)*1000)))/1000
					#print(item)
				elif col == 1:
					item = self.line*3.5 	# 3.5 ohm is the resistance of the heater
				elif col == 2:
					item = self.current_depth
				else:
                                        item = self.line
					
				self.worksheet.write(row, col, item)
			row = row +1
			#print('writing data')
			#time.sleep(1)
			
if __name__ == '__main__':
	try:	
		obj = datalog()
		obj.logging()
	except KeyboardInterrupt:
		obj.workbook.close()
		print("Shutting down program!!")
		
