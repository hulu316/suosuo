#!/usr/bin/env python
# encoding=UTF-8

import wtforms
from wtforms import validators
from wtforms import TextField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField

from wtforms_tornado import Form


class LoginForm(Form):
    email = TextField(u'邮箱', validators=[validators.required(), validators.email(), validators.Length(min=4, max=25)])
    password = PasswordField(u'密码', validators=[validators.required(), validators.Length(min=6, max=35)])
    remember = BooleanField(u'记住我', default=False)
    submit = SubmitField(u'登陆')
