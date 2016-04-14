#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from src.lib.jianshu_parser.base import BaseParser
from src.lib.jianshu_parser.content.jianshu_article import JianshuArticle
from src.lib.jianshu_parser.info.jianshu_author import JianshuAuthorInfo


class JianshuParser(BaseParser):
    u"""
    获得jianshu_info表中所需的内容
    """
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')
        self.article_parser = JianshuArticle(self.dom)
        return

    def get_jianshu_info_list(self):
        author_parser = JianshuAuthorInfo()     # jianshu_author表中的信息
        author_parser.set_dom(self.dom)
        return [author_parser.get_info()]
