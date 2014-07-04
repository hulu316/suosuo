#!/usr/bin/env python
# encoding=UTF-8

import wtforms
from wtforms import validators
from wtforms import TextField
from wtforms import SubmitField

from wtforms_tornado import Form


class CnameForm(Form):
    cname = TextField(u'频道名', validators=[validators.required(), validators.Length(min=1, max=64)])
    submit = SubmitField(u'确认')
