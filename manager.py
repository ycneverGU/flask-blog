#!/usr/bin/env python
# coding=utf-8
import os
from flask_script import Manager
from app import create_app,db 
from flask_migrate import Migrate,MigrateCommand
app = create_app(os.getenv('YCNGU_CONFIG') or 'default') 
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


@manager.command
def test():
    pass


@manager.command
def deploy():
    from app.models import Role
    upgrade()
    Role.seed()

if __name__ == '__main__':
    manager.run()
 #  app.run(debug=True)
