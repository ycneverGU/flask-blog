#!/usr/bin/env python
# coding=utf-8

import serial
import time
from ..models import charts
from .. import db
s = serial.Serial('/dev/ttyUSB0',115200)
#s = serial.Serial('/dev/ttyS0',115200)
print('start print')

def port():
    print('enter port')
    while True:
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
        time.sleep(2) 
        wendu=[]
        shidu=[]
        mq2=[]
        #print('leave sleep')



port()

