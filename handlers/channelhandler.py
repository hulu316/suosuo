#!/usr/bin/env python
# encoding=UTF-8

from itertools import imap

import tornado.web
import tornado.gen
from tornado.escape import json_encode
from tornado.escape import json_decode

import tornadoredis
from models import CONNECTION_POOL
import handlers
from handlers.basehandler import BaseHandler
from forms.cnameform import CnameForm


class ChatHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        uname = self.current_user
        cname = self.get_argument('cname', u'同一个世界')
        client = tornadoredis.Client(connection_pool=CONNECTION_POOL)
        length = yield tornado.gen.Task(client.hget, 'subchannels:%s' % uname, cname)
        if not length:
            # 这种恶意行为暂且认为是少数，以后可以通过屏蔽IP处理
            raise tornado.web.HTTPError(404)
        if length == '0':
            messages = ['欢迎光临 %s 频道！' % cname]
        else:
            messages = yield tornado.gen.Task(client.lrange, 'messages:%s' % cname, -int(length)-1, -1)
            messages = map(lambda x: '%s: %s' % (x['name'], x['msg']), imap(json_decode, messages))
            yield tornado.gen.Task(client.hset, 'subchannels:%s' % uname, cname, 0)
        channels = yield tornado.gen.Task(client.hgetall, 'subchannels:%s' % uname)
        self.render('channel/chat.html', channels=channels, messages=messages)

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        uname = self.current_user
        cname = self.get_argument('cname', u'同一个世界')
        client = tornadoredis.Client(connection_pool=CONNECTION_POOL)
        ret = yield tornado.gen.Task(client.hget, 'subchannels:%s' % uname, cname)
        if not ret:
            # 这种恶意行为暂且认为是少数，以后可以通过屏蔽IP处理
            raise tornado.web.HTTPError(404)

        msg = self.get_argument('msg', '')
        data = json_encode({'name': uname, 'msg': msg, 'cname': cname, 'badge': 0})
        yield tornado.gen.Task(client.publish, cname, data)
        self.finish()


class CreateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        form = CnameForm()
        self.render('channel/create.html', form=form)

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        form = CnameForm(self.request.arguments)
        if form.validate():
            client = tornadoredis.Client(connection_pool=CONNECTION_POOL)
            ismember = yield tornado.gen.Task(client.sismember, 'channelset', form.cname.data)
            if not ismember:
                with client.pipeline(transactional=True) as pipe:
                    pipe.hset('subchannels:%s' % self.current_user, form.cname.data, 0)
                    pipe.sadd('subunames:%s' % form.cname.data, self.current_user)
                    pipe.sadd('channelowner:%s' % self.current_user, form.cname.data)
                    pipe.sadd('channelset', form.cname.data)
                    yield tornado.gen.Task(pipe.execute)
                self.redirect('/channel/chat?cname=%s' % form.cname.data)
                return
            else:
                form.errors['invalid'] = True
        self.render('channel/create.html', form=form)


class SubscribeHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        cname = self.get_argument('cname', None)
        if not cname:
            raise tornado.web.HTTPError(404)

        client = tornadoredis.Client(connection_pool=CONNECTION_POOL)
        ismember = yield tornado.gen.Task(client.sismember, 'channelset', cname)
        if not ismember:
            raise tornado.web.HTTPError(404)
        ret = yield tornado.gen.Task(client.sadd, 'subunames:%s' % cname, self.current_user)
        if ret:
            yield tornado.gen.Task(client.hset, 'subchannels:%s' % self.current_user, cname, 0)

        self.redirect('/channel/chat?cname=%s' % cname)
