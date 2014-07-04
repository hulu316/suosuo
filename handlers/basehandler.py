#!/usr/bin/env python
# encoding=UTF-8

import tornado
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    # We can use self.current_user to get the user
    def get_current_user(self):
        uname = self.get_secure_cookie('uname')
        return uname

    def write_error(self, status_code, **kwargs):
        if not self.settings.get('debug'):
            if status_code == 404:
                return self.render('error/404.html')
            elif status_code == 401:
                return self.render('error/401.html')
            else:
                return self.render('error/500.html')
        else:
            super(BaseHandler, self).write_error(status_code, **kwargs)
