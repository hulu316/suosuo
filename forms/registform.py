#!/usr/bin/env python
# encoding=UTF-8

import wtforms
from wtforms import validators
from wtforms import TextField
from wtforms import PasswordField
from wtforms import SubmitField

from wtforms_tornado import Form


class RegistForm(Form):
    email = TextField(u'邮箱', validators=[validators.required(), validators.email(), validators.Length(min=4, max=25)])
    password = PasswordField(u'输入密码', [
        validators.Required(),
        validators.Length(min=6, max=35),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField(u'确认密码')
    submitButton = SubmitField(u'注册')
