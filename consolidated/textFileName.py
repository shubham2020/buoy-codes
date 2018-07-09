# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 12:19:33 2018

@author: Shubham Pathak
"""

import time

class date:
    def __init__(self, add = ''):
        self.add = add
        self.name = ''
        self.loc = '/home/pi/buoy-codes/data files/'
        
        
    def dateStamp(self):
        t = time.ctime(time.time())
        self.name = str(self.loc + self.add+ t + '.txt')
        return (self.name)

if __name__=='__main__':
    dt = date()
    dt.dateStamp()
    