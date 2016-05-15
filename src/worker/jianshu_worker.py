#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from src.tools.http import Http
from src.tools.match import Match

from src.worker.page_worker import PageWorker
from src.lib.jianshu_parser.jianshu_parser import JianshuParser

from src.lib.parser_tools import ParserTools


class JianshuAuthorWorker(PageWorker):
    u"""
    for jianshu author
    """
    def create_save_config(self):
        config = {
            'jianshu_article': self.answer_list,
            'jianshu_info': self.question_list
        }
        return config

    def parse_content(self, content):
        parser = JianshuParser(content)
        self.answer_list += parser.get_answer_list()

    @staticmethod
    def parse_get_article_list(article_list_content):
        u"""
        获得每一篇博客的链接组成的列表
        :param article_list_content: 有博文目录的href的页面
        :return:
        """
        soup = BeautifulSoup(article_list_content, "lxml")
        article_href_list = []

        article_list = soup.select('h4.title a')
        for item in range(len(article_list)):
            article_href = 'http://www.jianshu.com' + str(ParserTools.get_attr(article_list[item], 'href'))
            article_href_list.append(article_href)
        return article_href_list

    def get_jianshu_question_list(self, target_url):
        u"""
        get jianshu_info, article_num, article_list
        :param target_url:
        :return:
        """
        index_content = Http.get_content(target_url)
        parser = JianshuParser(index_content)
        self.question_list += parser.get_extra_info()
        article_num = self.question_list[0]['article_num']      # not collection, only one author
        article_list = self.parse_get_article_list(index_content)
        return article_num, article_list

    def create_work_set(self, target_url):
        u"""
        根据target_url(例:http://www.jianshu.com/users/b1dd2b2c87a8/latest_articles)的内容,
        先获得creator_id, 再根据文章的数目, 获得页面数, 依次打开每个页面, 将文章的地址放入work_set中
        :param target_url:
        :return:
        """
        if target_url in self.task_complete_set:
            return
        id_result = Match.jianshu_author(target_url)
        jianshu_id = id_result.group('jianshu_id')
        article_num, article_list = self.get_jianshu_question_list(target_url)
        self.task_complete_set.add(target_url)
        if article_num % 9 != 0:
            page_num = article_num/9 + 1      # 9 href on one page
        else:
            page_num = article_num / 9

        for item in article_list:
            self.work_set.add(item)
        for page in range(page_num-1):          # page+2, don't need to get the first page
            url = 'http://www.jianshu.com/users/{}/latest_articles?page={}'.format(jianshu_id, page+2)
            content_article_list = Http.get_content(url)
            article_list = self.parse_get_article_list(content_article_list)
            for item in article_list:
                self.work_set.add(item)
        return


class JianshuCollectionWorker(PageWorker):
    u"""
    for jianshu collection
    """



