import sys
from select import select

print "Press any key to configure or wait 5 seconds..."
timeout = 5
rlist, wlist, xlist = select([sys.stdin], [], [], timeout)

if rlist:
    print "Config selected..."
else:
    print "Timed out..."
    
print "configure done"