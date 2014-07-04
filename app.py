#!/usr/bin/env python
# encoding=UTF-8

import os

import tornado
import tornado.web

import handlers
from handlers.mainhandler import MainHandler
from handlers.loginhandler import LoginHandler
from handlers.logouthandler import LogoutHandler
from handlers.registhandler import RegistHandler
from handlers.channelhandler import ChatHandler
from handlers.channelhandler import CreateHandler
from handlers.channelhandler import SubscribeHandler
from handlers.abouthandler import AboutHandler
from handlers.longpollinghandler import LongPollingHandler


HANDLERS = [
    (r'/', MainHandler),
    (r'/account/login', LoginHandler),
    (r'/account/logout', LogoutHandler),
    (r'/account/regist', RegistHandler),
    (r'/channel/chat', ChatHandler),
    (r'/channel/create', CreateHandler),
    (r'/channel/subscribe', SubscribeHandler),
    (r'/longpolling', LongPollingHandler),
    (r'/about', AboutHandler),
]

SETTINGS = {
    'cookie_secret': 'Dhc5T+2OQDavaTvxvmg+keaZ/AcSiEArkOa+1+oElSQ=',
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'login_url': '/account/login',
    'xsrf_cookies': True,
    'debug': True,
}

application = tornado.web.Application(HANDLERS, **SETTINGS)

