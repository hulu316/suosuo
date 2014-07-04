#!/usr/bin/env python
# encoding=UTF-8

import tornado
import tornado.web

import tornadoredis
import handlers
from handlers.basehandler import BaseHandler
from models.manager import Manager


class LongPollingHandler(BaseHandler):
    def initialize(self):
        self._manager = Manager.instance()

    @tornado.web.asynchronous
    def post(self):
        uname = self.current_user
        cname = self.get_argument('cname', u'同一个世界')
        self._manager.add_handler(uname, cname, self.send_data)

    def send_data(self, data):
        if self.request.connection.stream.closed():
            self._manager.remove_handler(self.current_user)
            return
        self.finish(str(data))

    def on_message(self, msg):
        if msg.kind == 'message':
            self.send_data(str(msg.body))
        elif msg.kind == 'unsubscribe':
            self.unsubscribe()
        elif msg.kind == 'disconnect':
            print 'client disconnect'

    def unsubscribe(self):
        pass

    #def on_finish(self):
        #uname = self.current_user
        #self._manager.remove_handler(uname)
        #if self.client.subscribed:
            #self.client.unsubscribe(u'同一个世界')

    def on_connection_close(self):
        uname = self.current_user
        self._manager.remove_handler(uname)
        #if self.client.subscribed:
            #self.client.unsubscribe(u'同一个世界')
