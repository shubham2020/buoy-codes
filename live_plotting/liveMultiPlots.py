import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

def animate(i):
#========================================================================================================#
    # Part for subplot 1 starts here
    graph_data1 = open('/home/pi/buoy-codes/data files/errorData1(5July18).txt','r').read()
    lines1 = graph_data1.split('\n')
    #print(lines)
    xs1 = []
    ys1 = []
    x1= y1=0
    for line1 in lines1:
        if len(line1)>1:
            x1,y1 = line1.split(',')
        x1 = int(x1)
        y1 = -float(int(float(y1)*10)/10) # added -ve sign for showing depth in downward direction
        #print(x,y)
        xs1.append(x1)
        ys1.append(y1)
    ax1.clear()
    ax1.plot(xs1, ys1)
    ax1.set_title('Error status')
    ax1.set_ylabel('Error (in cm)')
    #ax1.set_xlabel('time steps')
    #Part for subplot 1 ends here
#========================================================================================================#
    #Part for subplot 2 starts here
    graph_data2 = open('/home/pi/buoy-codes/data files/pwmData1(5July18).txt','r').read()
    lines2 = graph_data2.split('\n')
    #print(lines)
    xs2 = []
    ys2 = []
    x2= y2=0
    for line2 in lines2:
        if len(line2)>1:
            x2,y2 = line2.split(',')
        x2 = int(x2)
        y2 = -float(int(float(y2)*10)/10) # added -ve sign for showing depth in downward direction
        #print(x,y)
        xs2.append(x2)
        ys2.append(y2)
    ax2.clear()
    ax2.plot(xs2, ys2)
    ax2.set_title('PWM status')
    ax2.set_ylabel('PWM in %age')
    ax2.set_xlabel('time steps')
    #Part for subplot 2 ends here
#========================================================================================================#
	
ani = animation.FuncAnimation(fig, animate, interval=1000) #for 1 sec delay 1000
plt.show()
