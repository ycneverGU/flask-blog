#!/usr/bin/env python
# coding=utf-8
from os import path
from werkzeug.routing import BaseConverter
from flask import Flask,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from flask_login import LoginManager,current_user
from flask_mail import Mail
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
from config import config
from flask_gravatar import Gravatar
db = SQLAlchemy()
mail = Mail()
moment = Moment()
bootstrap = Bootstrap()
toolbar = DebugToolbarExtension()
basedir = path.abspath(path.dirname(__file__))
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view ='auth.login'

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regx = item[0]


def create_app(config_name):
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    app.config.from_object(config[config_name])
    login_manager.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    Gravatar(app,size=64)
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    
    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path
    
    @app.template_test('author_selfid')
    def is_current_author(id):
        return id == current_user.id
   
    return app


