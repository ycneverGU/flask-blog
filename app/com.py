#!/usr/bin/env python
# coding=utf-8

import serial
import time
from .models import charts
from .  import db
#s = serial.Serial('/dev/ttyS0',115200)
print('start print')

def port(): 
    try:
        s = serial.Serial('/dev/ttyUSB0',115200)
    except Exception as e:
        print('except:',e)
        return None
    else:
        print('enter port') 
        s = serial.Serial('/dev/ttyUSB0',115200)
        for n in range(20):
            #print('enter while')
            count = s.inWaiting()
            #print('enter waiting')
            if count != 0:
                print('enter count')
                recv = s.read(count)
                #split=recv.split(':')
                #wendu=split[1][:2]
                #shidu=split[2][:2]
                #mq2=split[3][:2]
                recv1 = recv.split(':') 
                mq2 = recv1[1].split(',')[0]
                wendu = recv1[2].split(',')[0]
                shidu = recv1[3]
                newcharts = charts(wendu=wendu,shidu=shidu,MQ2=mq2)
                db.session.add(newcharts)
                db.session.commit()
                print('end commit')
                print(wendu,shidu,mq2)
                #s.write(recv)
            s.flushInput() 
            time.sleep(0.1)
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


