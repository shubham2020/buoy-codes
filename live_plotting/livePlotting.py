import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('/home/pi/buoy-codes/data files/testData 12-00(4 July 2018)mvg_avg.txt','r').read()
    lines = graph_data.split('\n')
    #print(lines)
    xs = []
    ys = []
    x= y=0
    for line in lines:
        if len(line)>1:
            x,y = line.split(',')
        x = int(x)
        y = float(int(float(y)*10)/10)
        #print(x,y)
        xs.append(x)
        ys.append(y)
    ax1.clear()
    ax1.plot(xs, ys)
    plt.suptitle('moving average window size 5') #add title for the graph all as you want
    plt.xlabel('time steps')
    plt.ylabel('depth in increments(in cm)')
	
ani = animation.FuncAnimation(fig, animate, interval=1000) #for 1 sec delay 1000
plt.show()
