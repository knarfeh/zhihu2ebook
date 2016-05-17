#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from src.tools.http import Http
from src.tools.match import Match
from src.worker.page_worker import PageWorker

from src.lib.parser_tools import ParserTools


class cnblogsAuthorWorker(PageWorker):
    u"""
    cnblogs author worker
    """
    @staticmethod
    def parse_max_page(content):
        pass

    def create_save_config(self):
        pass

    def parse_content(self, content):
        pass

    @staticmethod
    def parse_get_article_list(article_list_content):
        pass

    def get_csdnblog_question_list(self, index_content):
        pass

    def create_work_set(self, target_url):
        pass