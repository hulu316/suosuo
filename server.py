#!/usr/bin/env python
# encoding=UTF-8

import sys

import tornado
import tornado.ioloop
import tornado.options
from tornado.options import define
from tornado.options import options

from app import application


define("port", default=8000, help="run on the given port", type=int)


def main():
    tornado.options.parse_command_line()
    application.listen(options.port)
    print 'Starting HTTP server on port %d' % options.port
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    main()
