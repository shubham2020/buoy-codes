import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
#import threading

class plotLive():
    #style.use('fivethirtyeight')
    style.use('ggplot')
    
    def __init__(self,fname1, figname, pwm = 0, interval=1000):
        self.fig = plt.figure(figsize = (10,7.5))
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.interval = interval
        self.pwm = pwm
        self.fname1 = fname1 #current depth
        self.fig_name = figname
        self.ani = None
        #self.rw_lock = threading.Lock() #for reading and writing files
        #print(self.fname1, self.fname2)
        
    def animate(self,interval):
        #========================================================================================================#
            #Part for subplot 2 starts here
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
                x1 = int(x1)
                y1 = float(y1)#float(int(float(y2)*10)/10) 
                #print(x,y)
                xs1.append(x1)
                ys1.append(y1)
            self.ax1.clear()
            self.ax1.plot(xs1, ys1)
            #self.ax2.set_title('PWM status for Kp = {} Kd = {} Ki = {}'.format(self.Kp,self.Kd,self.Ki))
            self.ax1.set_ylabel('current depth', fontsize = 12)
            self.ax1.set_xlabel('time (in secs)', fontsize = 12)
            file1.close()
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