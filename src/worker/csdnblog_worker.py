#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json  # 用于JsonWorker
import re

from bs4 import BeautifulSoup

from src.worker.page_worker import PageWorker
from src.lib.parser_tools import ParserTools


class csdnAuthorWorker(PageWorker):
    u"""
    csdn blog
    """
    @staticmethod
    def parse_max_page(content):
        u"""
        :param content: index page
        :return: max page
        """
        max_page = 1
        match_object = re.search(r'条数据  共(?P<page_num>[^/\n\r]*)页', content)
        if match_object is not None:
            max_page = match_object.group('page_num')
        return max_page

    def create_save_config(self):    # TODO
        config = {'csdnblog_article': self.answer_list, 'csdnblog_info': self.question_list}
        return config

    def parse_content(self, content):
        parser = CsdnBlogParser(content)
        self.answer_list += parser.get_answer_list