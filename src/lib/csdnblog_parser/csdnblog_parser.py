#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from src.lib.csdnblog_parser.base import BaseParser
from src.lib.csdnblog_parser.content.csdnblog_article import CsdnBlogArticle
from src.lib.csdnblog_parser.info.csdnblog_author import CsdnBlogAuthorInfo


class CsdnBlogParser(BaseParser):
    u"""
    get the info of table csdnblog_info, csdnblog_article
    """
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')
        self.article_parser = CsdnBlogArticle(self.dom)

    def get_csdnblog_info_list(self):
        author_parser = CsdnBlogAuthorInfo()
        author_parser.set_dom(self.dom)
        return [author_parser.get_info()]
