file = fopen('/home/pi/buoy-codes/data files/testData15-59(2 July 2018).txt','r')
fprintf(file, '%d%s%2.10f\n')
fclose(file)