#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import getopt
import sys  # 修改默认编码
import os   # 添加系统路径

from dynaconf import settings
from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedLoginException
from match import Match
from common import str2bool

client = ZhihuClient()

short_options = 'u:l:d'
long_options = ['url=', 'login=', 'debug']


help_info = 'Usage: ee-book [OPTION]... [URL]... \n\n'

help_info += """Starup options:
-d | --debug                    Show traceback and other debug info.
\n
"""

help_info += """Run options:
-u | --url <URL>                URL to download, if not setted, read from ReadList.txt(default)
"""



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


def test_question_worker(target_url):
    question_id = Match.question(target_url).group('question_id')
    print("question_id")
    question_obj = client.question(int(question_id))
    print(question_obj)
    print("question_obj raw_data???{}".format(question_obj.pure_data))
    print("type of raw_data???{}".format(type(question_obj.pure_data)))


def main():
    debug = str2bool(settings.DEBUG)
    _get_token()

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
    except getopt.GetoptError as err:
        log.error_log(u"Try ee-book --help for more options")
        sys.exit(2)

    for option, args in opts:
        if option in ('-d', '--debug'):
            print("Running in Debug mode...")
        elif option in ('-u', '--url'):
            url = args
            # test_question_worker(target_url=url)
            from worker import worker_factory
            worker_factory(client, 'question', url)
            # game = EEBook(recipe_kind="zhihu", url=url, debug=debug)
            # game.begin()
            sys.exit()


if __name__ == '__main__':
    print(settings.get('DEBUG'))
    main()
