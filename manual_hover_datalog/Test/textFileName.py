# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 12:19:33 2018

@author: Shubham Pathak
"""

import time
import re

class dateS:
    def __init__(self, add = ''):
        self.add = add
        self.name = ''
        self.loc = ''
        self.ext = ''
        
    def forFig(self):
        self.loc = '/home/pi/buoy-codes/graphs/'
        self.ext = '.jpg'
        
    def forText(self):
        self.loc = '/home/pi/buoy-codes/manual_hover_datalog/datalog/'
        self.ext = '.xlsx'
        
    def dateStamp(self):
        t = time.ctime(time.time())
        pattern = r":"  # : -> this was making the file name invalid
        t = re.sub(pattern,"-",t) #so replaced it with a hyphen and bingo it worked
        self.name = str(self.loc + self.add + t + self.ext)
        return (self.name)

if __name__=='__main__':
    dt = dateS()
    dt.forText()
    name = dt.dateStamp()
    print(name)
    
