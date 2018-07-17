import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
#import threading

class plotLive():
    #style.use('fivethirtyeight')
    style.use('ggplot')
    
    def __init__(self,fname0, fname1, fname2, figname, Kp = 0, Kd = 0, Ki = 0, interval=1000):
        self.fig = plt.figure(figsize = (10,7.5))
        self.ax1 = self.fig.add_subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.interval = interval
        self.fname1 = fname1 #current depth
        self.fname2 = fname2 #PWM
        self.fname0 = fname0 #desired depth
        self.fig_name = figname
        self.ani = 0
        #self.rw_lock = threading.Lock() #for reading and writing files
        #print(self.fname1, self.fname2)
        
    def animate(self,interval):
        #with self.rw_lock:
        #=======================================================================================================#
            # Part for subplotting the desired depth
            file0 = open(self.fname0,'r')
            graph_data0 = file0.read()
            lines0 = graph_data0.split('\n')
            #print(lines)
            xs0 = []
            ys0 = []
            x0=y0=0
            for line0 in lines0:
                if len(line0)>2:
                    x0,y0 = line0.split(',')
                    #print(x1,y1)
                x0 = int(x0)
                y0 = -float(y0)#float(int(float(y0)*10)/10) # added -ve sign for showing depth in downward direction
                #print(x,y)
                xs0.append(x0)
                ys0.append(y0)
            file0.close()
            # Part for desired depth ends here
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
                if len(line1)>2:
                    x1,y1 = line1.split(',')
                    #print(x1,y1)
                x1 = int(x1)
                y1 = -float(y1)#float(int(float(y1)*10)/10) # added -ve sign for showing depth in downward direction
                #print(x,y)
                xs1.append(x1)
                ys1.append(y1)
            self.ax1.clear()
            self.ax1.plot(xs1, ys1, 'g', label= 'current depth') #for current depth
            self.ax1.plot(xs0, ys0, 'b', label= 'desired depth') #for desired depth
            self.ax1.legend(loc = 'best', fontsize = 10)
            self.ax1.set_title('Depth & PWM status for Kp = {} Kd = {} Ki = {}'.format(self.Kp,self.Kd,self.Ki),
                               fontsize = 14)
            self.ax1.set_ylabel('depth (in cm)', fontsize = 12)
            #self.ax1.set_xlabel('time (in secs)', fontsize = 12)
            file1.close()
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
                if len(line2)>2:
                    x2,y2 = line2.split(',')
                x2 = int(x2)
                y2 = float(y2)#float(int(float(y2)*10)/10) 
                #print(x,y)
                xs2.append(x2)
                ys2.append(y2)
            self.ax2.clear()
            self.ax2.plot(xs2, ys2)
            #self.ax2.set_title('PWM status for Kp = {} Kd = {} Ki = {}'.format(self.Kp,self.Kd,self.Ki))
            self.ax2.set_ylabel('PWM in %age', fontsize = 12)
            self.ax2.set_xlabel('time (in secs)', fontsize = 12)
            file2.close()
            #Part for subplot 2 ends here
    #========================================================================================================#
    def action(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval = self.interval) #for 1 sec delay 1000
        plt.show()
        #print('number of times')
        self.fig.savefig(self.fig_name)
        
if __name__=='__main__':
    obj = plotLive('one.txt','two.txt')
    #ani = animation.FuncAnimation(obj.fig, obj.animate, obj.interval)
    #plt.show()
    obj.action()