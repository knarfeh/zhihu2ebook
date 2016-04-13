#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from bs4 import BeautifulSoup

from src.tools.http import Http
from src.tools.match import Match
from src.tools.config import Config
from src.worker.page_worker import PageWorker

from src.lib.sinablog_parser.sinablogparser import SinaBlogParser
from src.lib.parser_tools import ParserTools


class sinablogAuthorWorker(PageWorker):
    u"""
    Sinablog worker
    """
    @staticmethod
    def parse_max_page(content):
        u"""
        :param content: 博客目录的页面内容
        :return: max page
        """
        max_page = 1
        try:
             floor = content.index('">下一页</a>')
             floor = content.rfind('</a>', 0, floor)
             cell = content.rfind('>', 0, floor)
             max_page = int(content[cell + 1:floor])
        finally:
            return max_page

    def create_save_config(self):    # TODO
        config = {'sinablog_article': self.answer_list, 'sinablog_info': self.question_list, }
        return config

    def parse_content(self, content):
        parser = SinaBlogParser(content)
        self.answer_list += parser.get_answer_list()

    @staticmethod
    def parse_article_num(content):
        u"""

        :param target_url: 博客目录的content
        :return: 博文总数量
        """
        soup = BeautifulSoup(content, "lxml")
        article_num = soup.select('div.SG_connHead span em')
        article_num = article_num[0].get_text()
        article_num = article_num[1:-1]    # 去掉前后两个括号
        return article_num

    @staticmethod
    def parse_get_article_list(article_list_content):
        u"""
        获得每一篇博客的链接组成的列表
        :param article_list_content: 博文目录页面的内容
        :return:
        """
        soup = BeautifulSoup(article_list_content, "lxml")
        article_href_list = []

        article_list = soup.select('span.atc_title a')
        for item in range(len(article_list)):
            article_title = ParserTools.get_attr(article_list[item], 'href')
            article_href_list.append(article_title)

        return article_href_list

    def create_work_set(self, target_url):
        u"""
        根据博客首页的url, 首先通过re获得博客id, 然后根据博客"关于我"的页面的内容获得写入sinablog_info
        的数据(这部分理应不在这个函数中, 可以改进), 最后通过博客目录页面的内容, 获得每篇博文的地址,
        放入work_set中

        :param target_url: 博客首页的url
        :return:
        """
        if target_url in self.task_complete_set:
            return
        result = Match.sinablog_author(target_url)
        sinablog_author_id = int(result.group('sinablog_people_id'))

        href_article_list = 'http://blog.sina.com.cn/s/articlelist_{}_0_1.html'.format(sinablog_author_id)
        href_profile = 'http://blog.sina.com.cn/s/profile_{}.html'.format(sinablog_author_id)

        # ############下面这部分应该是SinaBlogAuthorWorker的内容, 写到sinablog_info, 暂时写在这, 以后再优化
        content_profile = Http.get_content(href_profile)

        parser = SinaBlogParser(content_profile)
        self.question_list += parser.get_sinablog_info_list()
        # Debug.logger.debug(u"create_work_set中的question_list是什么??" + str(self.question_list))
        # #############上面这部分应该是SinaBlogAuthorWorker的内容, 写到sinablog_info, 暂时写在这, 以后再优化

        # content_index = Http.get_content(href_index)
        content_article_list = Http.get_content(href_article_list)

        article_num = int(self.parse_article_num(content_article_list))
        if article_num % 50 != 0:
            page_num = article_num/50 + 1      # 博客目录页面, 1页放50个博客链接
        else:
            page_num = article_num / 50

        self.question_list[0]['article_num'] = article_num  # 这样的话, 每行只能放一个新浪博客地址!!!
        # 上面这行, 暂时只能这样写, 因为"关于我"的页面, 没有文章的数量

        self.task_complete_set.add(target_url)

        for page in range(page_num):
            url = 'http://blog.sina.com.cn/s/articlelist_{}_0_{}.html'.format(sinablog_author_id, page+1)
            content_article_list = Http.get_content(url)
            article_list = self.parse_get_article_list(content_article_list)
            for item in article_list:
                self.work_set.add(item)
            # self.work_set.add(article_list[0])
        return