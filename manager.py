#!/usr/bin/env python
# coding=utf-8
import os
from app import create_app, db
from app.models import User, Role, Permission,Post,Follow,Comment,Todolist
from flask_migrate import Migrate, MigrateCommand
app = create_app(os.getenv('YCNGU_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment,Todolist=Todolist)



if __name__ == '__main__':
  app.run()
