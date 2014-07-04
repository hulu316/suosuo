#!/usr/bin/env python
# encoding=UTF-8

from models import CONNECTION_POOL


class User(object):
    def __init__(self):
        self.client = tornadoredis.Client(connection_pool=CONNECTION_POOL)

    def has_registed(self, uname):
        pass

    def regist(self, uname, password):
        pass

    def verify(self, uname, password):
        pass
