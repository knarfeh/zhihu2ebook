# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.SinaBlog_parser.base import BaseParser
from src.lib.SinaBlog_parser.content.SinaBlogAuthor import SinaBloeAuthorInfo
from src.lib.SinaBlog_parser.content.SinaBlogArticle import SinaBlogArticle


class SinaBlogParser(BaseParser):
    u"""
    获得SinaBlog_Info表中所需的内容
    """
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')
        self.article_parser = SinaBlogArticle(self.dom)

        return

    def get_SinaBlog_info_list(self):
        author_parser = SinaBloeAuthorInfo()     # SinaBlog_Info表中的信息
        author_parser.set_dom(self.dom)
        return [author_parser.get_info()]

