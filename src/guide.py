# -*- coding: utf-8 -*-
import re

from src.tools.config import Config


def set_account():
    print u'#使用内置账号进行登陆#'
    # account = raw_input()
    account = None
    if account:
        while not re.search(r'\w+@[\w\.]{3,}', account):
            print u'抱歉，输入的账号不规范...\n请输入正确的知乎登录邮箱\n'
            print u'请重新输入账号，回车确认'
            account = raw_input()
        print u'请输入密码，回车确认'
        password = raw_input()
        while len(password) < 6:
            print u'密码长度不正确，密码至少6位'
            print u'请重新输入密码，回车确认'
            password = raw_input()
    else:
        account, password = Config.account, Config.password
    return account, password


def set_picture_quality():
    print u'图片模式为1'
    try:
        # quality = int(raw_input())
        quality = 1
    except ValueError as error:
        print error
        print u'数字转换错误。。。'
        print u'图片模式重置为标准模式，点击回车继续'
        quality = 1
        raw_input()
    if not (quality in [0, 1, 2]):
        print u'输入数值非法'
        print u'图片模式重置为标准模式，点击回车继续'
        quality = 1
        raw_input()
    return quality
