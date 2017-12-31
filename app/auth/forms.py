#!/usr/bin/env python
# coding=utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, Length
from ..models import User

class LoginForm(Form):
    username = StringField(label=u'用户名', validators=[DataRequired()])
    password = PasswordField(label=u'密码', validators=[DataRequired()])
    remember_me= BooleanField(u'记住我')
    sumit = SubmitField(label=u'提交')


class RegistrationForm(Form):
    email = StringField(u'邮箱地址', validators=[DataRequired(),
                                             Length(1, 64),
                                             Email()])

    username = StringField(u'用户名', validators=[DataRequired(),
                                               Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                      u'用户名必须由字母数、字数、下划线或 . 组成')])

    password = PasswordField(u'密码', validators=[DataRequired(),
                                                EqualTo('password2', message=u'密码必须一至')])

    password2 = PasswordField(u'确认密码', validators=[DataRequired()])

    submit = SubmitField(u'马上注册')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError(u'用户名已被使用')
