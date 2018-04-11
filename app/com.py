#!/usr/bin/env python
# coding=utf-8

import serial
import time
from .models import charts
from .  import db
s = serial.Serial('/dev/ttyUSB0',115200)
#s = serial.Serial('/dev/ttyS0',115200)
print('start print')

def port():
    print('enter port')
    for n in range(2):
        #print('enter while')
        count = s.inWaiting()
        #print('enter waiting')
        if count != 0:
            #print('enter count')
            recv = s.read(count)
            split=recv.split(':')
            wendu=split[1][:2]
            shidu=split[2][:2]
            mq2=split[3][:2]
            newcharts = charts(wendu=wendu,shidu=shidu,MQ2=mq2)
            db.session.add(newcharts)
            db.session.commit()
            print(wendu,shidu,mq2)
            #s.write(recv)
        s.flushInput() 
        wendu=[]
        shidu=[]
        mq2=[]
        #print('leave sleep')


def port2():
    s = serial.Serial('/dev/ttyUSB0', 115200)
    print('enter port')
        #print('enter while')
    #print('enter waiting')
    for n in range(2):
        count = s.inWaiting()
        if count != 0:
            print('enter count')
            recv = s.read(count)
            split = recv.split(':')
            wendu = split[1][:2]
            shidu = split[2][:2]
            mq2 = split[3][:2]
            print(wendu, shidu, mq2)
            # s.write(recv)
        s.flushInput()
        time.sleep(1)
        wendu = []
        shidu = []
        mq2 = []

port2()

