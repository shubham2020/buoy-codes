import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

class plotLive():
    style.use('fivethirtyeight')
    
    def __init__(self, fname1, fname2, Kp = 0, Kd = 0, Ki = 0, interval=1000):
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.interval = interval
        self.fname1 = fname1
        self.fname2 = fname2
        self.ani = 0
        #print(self.fname1, self.fname2)
        
    def animate(self, interval):
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
            y1 = float(int(float(y1)*10)/10) # added -ve sign for showing depth in downward direction
            #print(x,y)
            xs1.append(x1)
            ys1.append(y1)
        self.ax1.clear()
        self.ax1.plot(xs1, ys1)
        self.ax1.set_title('Error status for Kp = {} Kd = {} Ki = {}'.format(self.Kp,self.Kd,self.Ki))
        self.ax1.set_ylabel('Error (in cm)')
        file1.close()
        #ax1.set_xlabel('time steps')
        #Part for subplot 1 ends here
    #========================================================================================================#
        #Part for subplot 2 starts here
        file2 = open(self.fname2,'r')
        graph_data2 = file2.read()
        lines2 = graph_data2.split('\n')
        #print(lines)
        xs2 = []
        ys2 = []
        x2= y2=0
        for line2 in lines2:
            if len(line2)>1:
                x2,y2 = line2.split(',')
            x2 = int(x2)
            y2 = float(int(float(y2)*10)/10) # added -ve sign for showing depth in downward direction
            #print(x,y)
            xs2.append(x2)
            ys2.append(y2)
        self.ax2.clear()
        self.ax2.plot(xs2, ys2)
        self.ax2.set_title('PWM status for Kp = {} Kd = {} Ki = {}'.format(self.Kp,self.Kd,self.Ki))
        self.ax2.set_ylabel('PWM in %age')
        self.ax2.set_xlabel('time (in millisecs)')
        file2.close()
        #Part for subplot 2 ends here
    #========================================================================================================#
    def action(self):    
        self.ani = animation.FuncAnimation(self.fig, self.animate, self.interval) #for 1 sec delay 1000
        plt.show()
if __name__=='__main__':
    obj = plotLive('one.txt','two.txt')
    obj.action()