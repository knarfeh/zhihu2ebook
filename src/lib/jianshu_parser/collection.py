#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from src.lib.jianshu_parser.base import BaseParser
from src.lib.jianshu_parser.info.jianshu_collection import JianshuCollectionInfo


class JianshuCollectionParser(BaseParser):
    def get_extra_info(self):
        author_parser = JianshuCollectionInfo()     # jianshu_author表中的信息
        author_parser.set_dom(self.dom)
        return author_parser.get_info()
