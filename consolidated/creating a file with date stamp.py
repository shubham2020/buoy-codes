# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 12:19:33 2018

@author: Shubham
"""

import time
import re

t = time.ctime(time.time())
pattern = r":"  # : -> this was making the file name invalid
new_t = re.sub(pattern,"-",t) #so replaced it with a hyphen and bingo it worked
name = str(new_t+'.txt')
file = open(name,'a+')
msg = "How was that??"
file.write(msg)
file.close()