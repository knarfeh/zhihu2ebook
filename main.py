#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import os

from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedLoginException
from match import Match, get_url_type
from common import str2bool
from worker import worker_factory

client = ZhihuClient()

URL = os.getenv('URL', 'https://zhuanlan.zhihu.com/newsql')


def _get_token():
    # TODO: get from inner api
    try:
        client.load_token(os.getcwd() + '/ZHIHUTOKEN.pkl')
        print("Got zhihutoken")
    except IOError:
        print("Please login first")
        sys.exit()
    except NeedLoginException:
        print("Login information expired, please login first")


def main():
    # _get_token()
    
    url_type = get_url_type(URL)
    if url_type == "unknown":
        print("Unsupported url: {}".format(URL))
        return

    worker_factory(client, url_type, URL)


if __name__ == '__main__':
    main()
