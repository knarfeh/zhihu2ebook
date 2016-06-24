#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from eventlet.greenpool import GreenPool
from config import Config


class Control(object):
    thread_pool = GreenPool()

    @staticmethod
    def control_center(argv, test_flag):
        max_try = Config.max_try
        for time in range(max_try):
            if test_flag:
                if Config.debug:
                    Control.debug_control(argv)
                else:
                    Control.release_control(argv)
        return

    @staticmethod
    def debug_control(argv):
        for item in argv['iterable']:
            argv['function'](item)
        return

    @staticmethod
    def release_control(argv):
        try:
            for _ in Control.thread_pool.imap(argv['function'], argv['iterable']):
                pass
        except Exception:
            # 报错全部pass掉
            # 等用户反馈了再开debug查
            pass
        return
