#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from src.lib.parser_tools import ParserTools
from src.tools.debug import Debug


class JianshuCollectionInfo(ParserTools):
    u"""
    对 http://www.jianshu.com/collection/e83275c61b78 这样的页面进行解析, 得到简书某专题的基本信息
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        self.info = {}
        self.dom = None
        return

    def set_dom(self, dom):
        if dom:
            self.dom = dom
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        Debug.logger.debug(u"Getting jianshu collection info...")
        self.parse_base_info()         # collection title, fake_id, real_id, description, follower
        # self.parse_detail_info()     # TODO ?
        return self.info

    def parse_base_info(self):
        self.parse_title()
        self.parse_collection_fake_id()
        self.parse_collection_real_id()
        self.parse_description()
        self.parse_follower()

    def parse_title(self):
        title = None
        if not title:
            Debug.logger.debug(u'专题标题未找到')
            # return
        self.info['title'] = 'testtesttest'

    def parse_collection_fake_id(self):
        self.info['collection_fake_id'] = 'testlalala'

    def parse_collection_real_id(self):
        self.info['collection_real_id'] = 'tsdfsaf'

    def parse_description(self):
        pass

    def parse_follower(self):
        pass

