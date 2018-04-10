#!/usr/bin/env python
# coding=utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))

a = os.path.join(basedir,'data-dev.sqlite')
print a

b = 'sqlite:///' + a

print b
