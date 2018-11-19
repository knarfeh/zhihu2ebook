# coding=utf-8

from __future__ import unicode_literals, print_function

import os

from zhihu_oauth import ZhihuClient


TOKEN_FILE = 'ZHIHUTOKEN.pkl'


client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)
