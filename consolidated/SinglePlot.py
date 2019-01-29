import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

class plotLive():
    style.use('fivethirtyeight')
    
    def __init__(self, fname1, figname, interval=1000): #first depth then PWM
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        #self.ax2 = self.fig.add_subplot(2,1,2)
        self.interval = interval
        self.fname1 = fname1
        #self.fname2 = fname2
        self.fig_name = figname
        self.ani = 0
        #print(self.fname1, self.fname2)
        
    def animate(self,interval):
    #========================================================================================================#
        # Part for subplot 1 starts here
        file1 = open(self.fname1,'r')
        graph_data1 = file1.read()
        lines1 = graph_data1.split('\n')
        #print(lines)
        xs1 = []
        ys1 = []
        x1= y1=0
        for line1 in lines1:
            if len(line1)>1:
                x1,y1 = line1.split(',')
                #print(x1,y1)
            x1 = int(x1)
            y1 = float(int(float(y1)*10))/10 
            #print(x,y)
            xs1.append(x1)
            ys1.append(y1)
        self.ax1.clear()
        self.ax1.plot(xs1, ys1)
        self.ax1.set_title('Velocity Status')
        self.ax1.set_ylabel('Velocity (cm/s)')
        file1.close()
        #ax1.set_xlabel('time steps')
        #Part for subplot 1 ends here
    #========================================================================================================#
    def action(self):
        #self.ani = animation.FuncAnimation(self.fig, self.animate, interval = self.interval) #for 1 sec delay 1000
        plt.show()
        #print('number of times')
        self.fig.savefig(self.fig_name)
        
if __name__=='__main__':
    file_name = '/home/pi/buoy-codes/data files/curr depth on Tue Nov 20 14-00-50 2018.txt'
    figure_name = '/home/pi/buoy-codes/graphs/Open-loop Plot on Tue Nov 20 14-00-50 2018.jpg'
    obj = plotLive(file_name, figure_name)
    #ani = animation.FuncAnimation(obj.fig, obj.animate, obj.interval)
    #plt.show()
    obj.action()

