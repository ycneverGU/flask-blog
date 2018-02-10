#!/usr/bin/env python
# coding=utf-8

from ..models import Role, User
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class PostForm(Form):
    title = StringField(label=u'标题', validators=[DataRequired(u'标题不能为空')])
    body = TextAreaField(label=u'内容', validators=[DataRequired(u'内容不能为空')])
    submit = SubmitField(u'提交')


class CommentForm(Form):
    body = TextAreaField(label=u'评论', validators=[DataRequired()])
    submit = SubmitField(u'发表')


class NameForm(Form):
    name = StringField(u'你的名字？', validators=[DataRequired()])
    submit = SubmitField(u'提交')


class EditProfileForm(Form):
    name = StringField(u'名字', validators=[Length(0, 64)])
    location = StringField(u'地点', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    username = StringField(u'用户名', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               u'用户名只能包含数字，字母，点或者下划线.')])
    confirmed = BooleanField(u'Confirmed')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'名字', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被注册.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'名字已被使用.')
