#!/usr/bin/env python
# coding=utf-8
import os
from app import create_app, db
from app.models import User, Role, Permission, Post, Follow, Comment, Todolist, charts
from flask_migrate import Migrate, MigrateCommand
import serial
import time
app = create_app(os.getenv('YCNGU_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment, Todolist=Todolist)


@app.cli.command()
def seed():
    superadmin = User(
        name='admin',
        username='admin',
        email='guon691@163.com',
        role_id=2,
        confirmed=1,
        locale='zh',
        location='default')
    superadmin.password = '1234567890'
    superadmin.avatar_hash = superadmin.gravatar_hash()
    db.session.add(superadmin)
    db.session.commit()

def port():
    s = serial.Serial('/dev/ttyUSB0', 115200)
    print('enter port')
    while True:
        #print('enter while')
        count = s.inWaiting()
        #print('enter waiting')
        if count != 0:
            #print('enter count')
            recv = s.read(count)
            split = recv.split(':')
            wendu = split[1][:2]
            shidu = split[2][:2]
            mq2 = split[3][:2]
            newcharts = charts(wendu=wendu, shidu=shidu, MQ2=mq2)
            db.session.add(newcharts)
            db.session.commit()
            print(wendu, shidu, mq2)
            # s.write(recv)
        s.flushInput()
        time.sleep(2)
        wendu = []
        shidu = []
        mq2 = []


if __name__ == '__main__':
    app.run()
