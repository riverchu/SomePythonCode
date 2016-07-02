#!/usr/bin/pythontest
import time

s='hello'
l=[1,2,3,'a','b']
t=(4,5,6,'x','y')

for x in range(20):
    print x
    time.sleep(1)
    if(x==4):
        continue
    if(x==6):
        break
    print '#'*50
else: 
    print 'ending'
