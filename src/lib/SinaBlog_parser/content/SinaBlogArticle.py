# -*- coding: utf-8 -*-
from src.lib.SinaBlog_parser.tools.parser_tools import ParserTools
from src.tools.match import Match
from src.tools.debug import Debug


class SinaBlogArticle(ParserTools):
    def __init__(self, dom=None):
        if dom:
            # Debug.logger.debug(u"SinaBlogArticle中,YESSSSSSSSSSSSSSSSSS")
            pass
        self.set_dom(dom)
        self.info = {}
        return

    def set_dom(self, dom):
        if dom:
            self.dom = dom
        return

    def get_info(self):
        answer_info = self.parse_info()
        return answer_info

    def parse_info(self):
        self.parse_author_id()
        self.parse_author_name()
        self.parse_article_id()
        self.parse_article_title()
        self.parse_answer_content()     # 获得博文的内容
        # self.parse_href()
        # self.parse_comment()          # TODO
        # self.parse_publish_data()     # TODO
        return self.info

    def parse_answer_content(self):
        u"""
        获得博文的内容
        :return:
        """
        article_body = self.dom.find('div', class_='articalContent')
        # article_body = self.dom.find('div', class_='articalContent')
        # article_body = self.dom.find('div', id='sina_keyword_ad_area2')
        # article_body = self.dom.select('#sina_keyword_ad_area2')[0]
        # article_body = self.dom.select('div.articalContent')
        if not article_body:
            Debug.logger.debug(u"博文内容没有找到")
            return
        article_body = str(article_body)
        self.info['content'] = article_body


    def parse_author_id(self):   # TODO 这个部分可以不重复的
        u"""
        获得author_id
        :return:
        """
        author_id_href = False
        author_id = self.dom.select('div.blognavInfo span a')
        if author_id:
            author_id_href = ParserTools.get_attr(author_id[1], 'href')    # 因为creator_id[0]是首页的链接

        if not author_id_href:
            Debug.logger.debug(u"没有找到creator_id")
            # TODO
            return
        result = Match.SinaBlog_profile(author_id_href)
        SinaBlog_id = result.group('SinaBlog_people_id')
        self.info['author_id'] = SinaBlog_id

    def parse_author_name(self):
        u"""
        获得author的姓名
        :return:
        """
        author_name = self.dom.select('div.info_nm span strong')       # 获得creator_name
        if not author_name:
            Debug.logger.debug(u"没有找到博主姓名")
            # TODO: 变量命名可以改一下
            return
        author_name = author_name[0].get_text().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
        self.info['author_name'] = author_name

    def parse_article_id(self):
        u"""
        获得博文的id
        :return:
        """
        article_id = False
        id = self.dom.select('div.artical h2')
        if id:
            article_id = ParserTools.get_attr(id[0], 'id')
        if not article_id:
            Debug.logger.debug(u"没有找到博文的id")
            return
        article_id = article_id[2:]
        self.info['article_id'] = article_id

    def parse_article_title(self):
        u"""
        获得博文的标题
        :return:
        """
        article_title = False
        title = self.dom.select('div.articalTitle h2')
        if title:
            article_title = title[0].get_text()
        if not article_title:
            Debug.logger.debug(u"没有找到博文标题")
            return
        # 标题里如果出现&,<<这样的符号会出错
        self.info['title'] = article_title.replace('&', '&amp;').replace('<<', "《").replace('>>', "》")






