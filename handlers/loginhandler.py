#!/usr/bin/env python
# encoding=UTF-8

import tornado
import tornado.web
import tornado.gen

import tornadoredis
from models import CONNECTION_POOL
import handlers
from handlers.basehandler import BaseHandler
from forms.loginform import LoginForm


class LoginHandler(BaseHandler):
    #def initialize(self):
        #self.client = tornadoredis.Client(connection_pool=CONNECTION_POOL)

    def get(self):
        if self.current_user:
            self.redirect('/')
            return
        form = LoginForm()
        self.render('account/login.html', form=form)

    #@tornado.web.asynchronous
    #@tornado.gen.engine
    @tornado.gen.coroutine
    def post(self):
        form = LoginForm(self.request.arguments)
        if form.validate():
            client = tornadoredis.Client(connection_pool=CONNECTION_POOL)
            password = yield tornado.gen.Task(client.hget, 'userinfo:%s' % form.email.data, 'password')
            if password and password == form.password.data:
                self.set_secure_cookie('uname', form.email.data)
                self.redirect(self.get_argument('next', '/'))
                return
            else:
                form.errors['invalid'] = True
        #print form.email.errors
        #print form.password.errors
        self.render('account/login.html', form=form)
