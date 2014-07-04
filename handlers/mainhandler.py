#!/usr/bin/env python
# encoding=UTF-8

import tornado
import tornado.web

import handlers
from handlers.basehandler import BaseHandler


class MainHandler(BaseHandler):
    def get(self):
        self.render('site/index.html')

