#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from src.lib.jianshu_parser.base import BaseParser
from src.lib.jianshu_parser.info.jianshu_collection import JianshuCollectionInfo


class JianshuCollectionParser(BaseParser):

    def get_article_list(self):
        article_list = self.dom.select("div h4.title a")
        a_list = list()
        for item in article_list:
            a_list.append('http://jianshu.com' + self.get_attr(item, 'href'))
        return a_list

    def get_extra_info(self):
        author_parser = JianshuCollectionInfo()
        author_parser.set_dom(self.dom)
        return author_parser.get_info()
