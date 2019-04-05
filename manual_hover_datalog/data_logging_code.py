#############	System libraries	#################
import serial
import xlsxwriter
#############		End				#################

#############	User defined libraries	#############
import textFileName as tfn
import readSensor as rs
#############			End				#############

class datalog:
	def __init__(self):
		self.ser = serial.Serial('/dev/ttyACM0', 9600)		#object for getting handle of serial communication
		self.sensor_obj = rs.sensorRead() #can pass filter window size as an argument
        self.sensor_obj.initialization()
        print('Sensor initalized and calibrated')
        file_name_object = tfn.dateS('hovering data_log on ')
        file_name_object.forText()
        file_name = file_name_object.dateStamp()
        self.workbook = xlsxwriter.Workbook(file_name)
        self.worksheet = self.workbook.add_worksheet()
        
        self.current_depth = 0
        self.line = 0
        
    def logging(self):
		row = 0
		self.current_depth = self.sensor_obj.reading()
		if(ser.in_waiting >0):		#to check if the buffer has some data (its type is int)
			self.line = float(ser.readline())
		while 1:
			for col in range(2):
				if col == 0:
					item = self.current_depth
				else:
					item = self.line
				self.worksheet.write(row, col, item)
			row = row +1 
			
if __name__ == '__main__':
	obj = datalog()
	obj.logging()
				
		
