import sys
from select import select
	
while True:
	#print "Press any key to configure or wait 5 seconds..."
	timeout = 0.001
	rlist, wlist, xlist = select([sys.stdin],[],[],timeout)

	if rlist:
		name = input("Enter your name :-")
	else:
		continue
		#print "Timed out..."
	
