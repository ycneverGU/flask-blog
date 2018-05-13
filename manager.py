#!/usr/bin/env python
# coding=utf-8
import os
from app import create_app, db
from app.models import User, Role, Permission, Post, Follow, Comment, Todolist, charts
from flask_migrate import Migrate, MigrateCommand
import serial
import time
from threading import Thread
from app.scheduler import Scheduler
app = create_app(os.getenv('YCNGU_CONFIG') or 'default')
migrate = Migrate(app, db)

from app.com import port

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


if __name__ == '__main__':
    scheduler = Scheduler(5,port)
    scheduler.start()
    app.run()
    scheduler.stop()

