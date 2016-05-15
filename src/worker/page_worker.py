#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json  # 用于JsonWorker
import re

from src.tools.controler import Control
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match
from src.tools.config import Config

from src.lib.zhihu_parser.question import QuestionParser


class PageWorker(object):
    def __init__(self, task_list):
        self.task_set = set(task_list)
        self.task_complete_set = set()
        self.work_set = set()            # 待抓取网址池
        self.work_complete_set = set()   # 已完成网址池
        self.content_list = []           # 用于存放已抓取的内容

        self.answer_list = []
        self.question_list = []

        self.info_list = []
        self.extra_index_list = []
        self.info_url_set = self.task_set.copy()
        self.info_url_complete_set = set()

        # 添加扩展属性
        self.add_property()
        Config._load()          # TODO: 可能对性能有影响,有没有更好的方式?
        if Config.need_account:
            Debug.logger.debug("Need cookie")
            Http.set_cookie()
        else:
            Debug.logger.debug("Don't need cookie")
            Http.set_cookie('DontNeed')

    def add_property(self):

        return

    @staticmethod
    def parse_max_page(content):
        max_page = 1
        try:
            floor = content.index('">下一页</a></span>')
            floor = content.rfind('</a>', 0, floor)
            cell = content.rfind('>', 0, floor)
            max_page = int(content[cell + 1:floor])
            Debug.logger.info(u'答案列表共计{}页'.format(max_page))
        except:
            Debug.logger.info(u'答案列表共计1页')
        finally:
            return max_page

    def create_save_config(self):
        u"""
        key 即为表名
        :return:
        """
        config = {'Answer': self.answer_list, 'Question': self.question_list, }
        return config

    def clear_index(self):
        u"""
        用于在collection/topic中清除原有缓存
        """
        return

    def save(self):
        self.clear_index()
        save_config = self.create_save_config()
        for key in save_config:
            for item in save_config[key]:
                if item:
                    DB.save(item, key)
        DB.commit()
        return

    def start(self):
        self.start_catch_info()
        self.start_create_work_list()
        self.start_worker()
        self.save()
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url + '?nr=1&sort=created')
        if not content:
            return
        self.task_complete_set.add(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}?nr=1&sort=created&page={}'.format(target_url, page + 1)
            self.work_set.add(url)
        return

    def clear_work_set(self):
        self.work_set = set()
        return

    def start_create_work_list(self):
        self.clear_work_set()
        argv = {'func': self.create_work_set, 'iterable': self.task_set, }
        Control.control_center(argv, self.task_set)
        return

    def worker(self, target_url):
        if target_url in self.work_complete_set:
            # 自动跳过已抓取成功的网址
            return

        Debug.logger.info(u'开始抓取{}的内容'.format(target_url))
        content = Http.get_content(target_url)
        if not content:
            return
        from src.worker.sinablog_worker import sinablogAuthorWorker
        if isinstance(self, sinablogAuthorWorker):
            content = Match.fix_html(content=content, recipe_kind='sinablog_author')
        else:
            content = Match.fix_html(content=content)  # 需要修正其中的<br>标签，避免爆栈
        self.content_list.append(content)
        Debug.logger.debug(u'{}的内容抓取完成'.format(target_url))
        self.work_complete_set.add(target_url)
        return

    def parse_content(self, content):
        parser = QuestionParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()
        return

    def start_worker(self):
        u"""
        work_set是所有的需要抓取的页面(单篇的文章)
        :return:
        """
        a = list(self.work_set)
        a.sort()
        argv = {
            'func': self.worker,  # 所有待存入数据库中的数据都应当是list
            'iterable': a,
        }
        Control.control_center(argv, self.work_set)
        Debug.logger.info(u"所有内容抓取完毕，开始对页面进行解析")
        i = 0
        for content in self.content_list:
            i += 1
            Debug.print_in_single_line(u"正在解析第{}/{}张页面".format(i, self.content_list.__len__()))
            self.parse_content(content)
        Debug.logger.info(u"网页内容解析完毕")
        return

    def catch_info(self, target_url):
        return

    def start_catch_info(self):
        argv = {'func': self.catch_info, 'iterable': self.info_url_set, }
        Control.control_center(argv, self.info_url_set)
        return
