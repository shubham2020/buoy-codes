import matplotlib.pyplot as plt

try:
    data_d1 = open('/home/pi/shubham_pathak_codes/data D1','r')
    time = open('/home/pi/shubham_pathak_codes/time','r')
    t = (time.readlines())
    d1 =  (data_d1.readlines())
    print('Time\t\t\tData\t\t\tData Type')
    for i in range(len(t)):
        t[i] = int(t[i])
        d1[i] =  int(d1[i])
        x = type(d1[i])
        print('{}\t\t\t{}\t\t\t{}'.format(t[i],d1[i],x))
    #plt.plot(t,d1)
    plt.scatter(t,d1)
    plt.xlabel('time axis')
    plt.ylabel('data axis')
    plt.show()
except Exception as e:
    print(str(e))
