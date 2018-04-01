#!/usr/bin/env python
# coding=utf-8
from forgery_py import date
from random import randint, sample
from datetime import datetime
import time

data = {"data": [], "time": []}


def time2seconds(t):
    h, m, s = t.strip().split(":")
    return int(h) * 3600 + int(m) *60  + int(s)


def seconds2time(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


def randhms(st, et,times):
    sts = time2seconds(st)
    ets = time2seconds(et)
    rt = sample(range(sts,ets),times)
    rt.sort()
    return rt


def randdata():
    return {
        "shidu": randint(20, 35),
        "MQ2": randint(18, 27),
        "wendu": randint(23, 29),
        "time": []
    }


virtualtime = randhms("10:27:34","13:19:58",20)
p = []
for s in range(1, 20):
    p.append(randdata())

def out():    
    for n in range(len(p)):
        p[n]["time"]=time.strftime("%Y-%m-%d") + " " + seconds2time(virtualtime[n])
        print(p[n])
    return p





