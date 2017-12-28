#!/usr/bin/env python
# coding=utf-8

from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired

class PostForm(Form):
    title = StringField(label=u'标题',validators=[DataRequired(u'标题不能为空')])
    body = TextAreaField(label=u'内容',validators=[DataRequired(u'内容不能为空')])
    submit = SubmitField(u'提交')

class CommentForm(Form):
    body = TextAreaField(label=u'评论',validators=[DataRequired()])
    submit = SubmitField(u'发表')

