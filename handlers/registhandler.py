#!/usr/bin/env python
# encoding=UTF-8

import tornado
import tornado.web
import tornado.gen

import tornadoredis
from models import CONNECTION_POOL
import handlers
from handlers.basehandler import BaseHandler
from forms.registform import RegistForm


class RegistHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/')
            return
        form = RegistForm()
        self.render('account/regist.html', form=form)

    #@tornado.web.asynchronous
    #@tornado.gen.engine
    @tornado.gen.coroutine
    def post(self):
        form = RegistForm(self.request.arguments)
        if form.validate():
            client = tornadoredis.Client(connection_pool=CONNECTION_POOL)
            password = yield tornado.gen.Task(client.hget, 'userinfo:%s' % form.email.data, 'password')
            if not password:
                with client.pipeline(transactional=True) as pipe:
                    pipe.hset('subchannels:%s' % form.email.data, u'同一个世界', 0)
                    pipe.sadd('subunames:%s' % u'同一个世界', form.email.data)
                    pipe.hset('userinfo:%s' % form.email.data, 'password', form.password.data)
                    yield tornado.gen.Task(pipe.execute)
                    #print res, len(res)
                self.set_secure_cookie('uname', form.email.data)
                self.redirect(self.get_argument('next', '/'))
                return
            else:
                form.errors['invalid'] = True
        self.render('account/regist.html', form=form)
