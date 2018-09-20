# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 12:19:33 2018

@author: Shubham Pathak
"""

import time

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
        self.loc = '/home/pi/buoy-codes/data files/'
        self.ext = '.txt'
        
    def dateStamp(self, flag = 0):
        if flag == 0:
            self.forText()
        else:
            self.forFig()
        t = time.ctime(time.time())
        self.name = str(self.loc + self.add + t + self.ext)
        return (self.name)

if __name__=='__main__':
    dt = dateS()
    dt.forText()
    dt.dateStamp()
    