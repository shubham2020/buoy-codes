import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

def livePlot():
    style.use('fivethirtyeight')

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(i):
        graph_data = open('sensorData.txt','r').read()
        lines = graph_data.split('\n')
        #print(lines)
        xs = []
        ys = []
        for line in lines:
            if len(line)>1:
                x,y = line.split(',')
            #print(x,y)
            xs.append(x)
            ys.append(y)
        ax1.clear()
        ax1.plot(xs, ys)
            
    ani = animation.FuncAnimation(fig, animate, interval=1000) #for 1 sec delay 1000
    plt.show()
if __name__=="__main__":
    livePlot()