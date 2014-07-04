#!/usr/bin/env python
# encoding=UTF-8

import tornado
import tornado.web

import handlers
from handlers.basehandler import BaseHandler


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('uname')
        self.redirect('/')
