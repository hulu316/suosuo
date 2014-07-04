#!/usr/bin/env python
# encoding=UTF-8

import hashlib

import tornado.gen
from tornado.escape import json_encode
from tornado.escape import json_decode

import tornadoredis
from models import CONNECTION_POOL


class Manager(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Manager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._user_callback = {}
        self._channel_client = {}

    @staticmethod
    def instance():
        if not Manager._instance:
            Manager._instance = Manager()
        return Manager._instance

    def make_md5(self, string):
        return hashlib.md5(str(string)).hexdigest()

    @tornado.gen.coroutine
    def add_handler(self, uname, channel, callback=None):
        #channel_md5 = self.make_md5(channel)
        if channel not in self._channel_client:
            _client = tornadoredis.Client()
            _client.connect()
            yield tornado.gen.Task(_client.subscribe, channel)
            _client.listen(self.on_message)
            self._channel_client[channel] = _client
        self._user_callback[uname] = [channel, callback]

    def remove_handler(self, uname, channel=None):
        print 'Remove handler: %s' % uname
        self._user_callback.pop(uname, None)

    @tornado.gen.coroutine
    def on_message(self, msg):
        if msg.kind == 'message':
            data = json_decode(str(msg.body))
            cname = data['cname']
            client = tornadoredis.Client(connection_pool=CONNECTION_POOL)
            yield tornado.gen.Task(client.rpush, 'messages:%s' % cname, msg.body)
            unames = yield tornado.gen.Task(client.smembers, 'subunames:%s' % cname)
            print unames
            for uname in unames:
                if uname in self._user_callback:
                    channel, callback = self._user_callback[uname]
                    if channel == cname:
                        callback(msg.body)
                        continue
                    else:
                        # 如何提示未读消息
                        data['badge'] = 1
                        callback(json_encode(data))
                yield tornado.gen.Task(client.hincrby, 'subchannels:%s' % uname, cname, 1)
        else:
            pass
