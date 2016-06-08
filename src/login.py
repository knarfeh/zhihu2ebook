# -*- coding: utf-8 -*-
import cookielib
import os
import urllib2
import sys

from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedLoginException
from src.tools.extra_tools import ExtraTools
from src.tools.path import Path


class Login(object):
    def __init__(self, recipe_kind, from_ui=False):
        self.recipe_kind = recipe_kind
        self.cookieJar = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))
        urllib2.install_opener(self.opener)
        self.from_ui = from_ui

    def start(self):
        try:
            client = ZhihuClient()
            client.login_in_terminal()
            client.save_token(Path.ZHIHUTOKEN)
        except NeedLoginException:
            print u"Oops, please try again."
            sys.exit()
        return

    def get_cookie(self):
        filename = ExtraTools.md5(ExtraTools.get_time())
        with open(filename, 'w') as f:
            pass
        self.cookieJar.save(filename)
        with open(filename) as f:
            content = f.read()
        os.remove(filename)
        return content
