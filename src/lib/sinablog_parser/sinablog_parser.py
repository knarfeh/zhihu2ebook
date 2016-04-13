# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from src.lib.sinablog_parser.base import BaseParser
from src.lib.sinablog_parser.content.sinablog_article import SinaBlogArticle
from src.lib.sinablog_parser.info.sinablog_author import SinaBlogAuthorInfo


class SinaBlogParser(BaseParser):
    u"""
    获得sinablog_info表中所需的内容
    """
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')
        self.article_parser = SinaBlogArticle(self.dom)

        return

    def get_sinablog_info_list(self):
        author_parser = SinaBlogAuthorInfo()     # sinablog_info表中的信息
        author_parser.set_dom(self.dom)
        return [author_parser.get_info()]

