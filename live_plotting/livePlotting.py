import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('example.txt','r').read()
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
    plt.xlabel('time steps')
    plt.ylabel('depth in increments')
	
ani = animation.FuncAnimation(fig, animate, interval=1000) #for 1 sec delay 1000
plt.show()
