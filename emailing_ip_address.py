# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 22:32:15 2018

@author: Shubham
"""

import smtplib
import socket

#hostname = socket.gethostname()  #this code for windows
#IPAddr = socket.gethostbyname(hostname)


def get_ip_address(): #this code for raspberry pi
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

#msg = str('Your IP address is :- ' + get_ip_address())
#print(msg)

mail = smtplib.SMTP('smtp.gmail.com',587) # use SMTP_SSL(465 for ssl) or SMTP(587 for TLS) then starttls()
mail.ehlo() #ehlo for extended smtp severs while helo is for general ones
mail.starttls() #for data encryption of whatever comes next in the code
mail.login('rpi3.gpio@gmail.com','raspberrypi!@#')       
mail.sendmail('rpi3.gpio@gmail.com','pshubham.me@gmail.com',get_ip_address())
mail.close()
