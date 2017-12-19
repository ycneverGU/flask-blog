#!/usr/bin/env python
# coding=utf-8
from os import path
from werkzeug.routing import BaseConverter
from flask import Flask
from flask_nav import Nav
from flask_nav.elements import *
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from flask_login import LoginManager,current_user
db = SQLAlchemy()
nav = Nav()
bootstrap = Bootstrap()
basedir = path.abspath(path.dirname(__file__))
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view ='auth.login'
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regx = item[0]


def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    app.config.from_pyfile('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOW'] = True
    nav.register_element('top', Navbar('ycngu',
                                       View(u'主页', 'main.index'),
                                       View(u'关于', 'main.about'),
                                       View(u'项目', 'main.projects'),
                                       ))
   #Nav.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    from auth import auth as auth_blueprint
    from main import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    
    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    return app
