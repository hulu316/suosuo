#!/usr/bin/env python
# encoding=UTF-8

import handlers
from handlers.basehandler import BaseHandler


class AboutHandler(BaseHandler):
    def get(self):
        self.render('site/about.html')
