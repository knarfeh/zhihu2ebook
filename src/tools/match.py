# -*- coding: utf-8 -*-
import re

from src.tools.type import Type


class Match(object):
    @staticmethod
    def xsrf(content=''):
        xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', content)
        if xsrf:
            return '_xsrf=' + xsrf.group(0)
        return ''

    # zhihu
    @staticmethod
    def answer(content=''):
        return re.search(r'(?<=zhihu\.com/)question/(?P<question_id>\d{8})/answer/(?P<answer_id>\d{8})', content)

    @staticmethod
    def question(content=''):
        return re.search(r'(?<=zhihu\.com/)question/(?P<question_id>\d{8})', content)

    @staticmethod
    def author(content=''):
        return re.search(r'(?<=zhihu\.com/)people/(?P<author_id>[^/\n\r]*)', content)

    @staticmethod
    def collection(content=''):
        return re.search(r'(?<=zhihu\.com/)collection/(?P<collection_id>\d*)', content)

    @staticmethod
    def topic(content=''):
        return re.search(r'(?<=zhihu\.com/)topic/(?P<topic_id>\d*)', content)

    @staticmethod
    def article(content=''):
        return re.search(r'(?<=zhuanlan\.zhihu\.com/)(?P<column_id>[^/]*)/(?P<article_id>\d{8})', content)

    @staticmethod
    def column(content=''):
        return re.search(r'(?<=zhuanlan\.zhihu\.com/)(?P<column_id>[^/\n\r]*)', content)

    @staticmethod
    def html_body(content=''):
        return re.search('(?<=<body>).*(?=</body>)', content, re.S).group(0)

    # jianshu
    @staticmethod
    def jianshu_author(content=''):
        u"""

        :param content: jianshu个人主页的地址
        :return: re.match object
        """
        return re.search(r'(?<=jianshu\.com/users/)(?P<jianshu_id>[^/\n\r]*)(/latest_articles)', content)

    @staticmethod
    def jianshu_article_id(content=''):
        u"""

        :param content:
        :return:
        """
        return re.search(r'(?<=www\.jianshu\.com/p/)(?P<jianshu_article_id>[^/\n\r\']*)()', content)

    # sinablog
    @staticmethod
    def sinablog_author(content=''):
        u"""
        TODO: 这样的链接也是可以的: http://blog.sina.com.cn/1340398703, 以及这样的:
        http://blog.sina.com.cn/caicui
        :param content: Sina博客网址, 如:http://blog.sina.com.cn/u/1287694611
        :return:  re.match object
        """
        return re.search(r'(?<=blog\.sina\.com\.cn/u/)(?P<sinablog_people_id>[^/\n\r]*)', content)

    @staticmethod
    def sinablog_profile(content=''):
        u"""

        :param content: Sina博客"博客目录"的网址, 如:
            http://blog.sina.com.cn/s/articlelist_1287694611_0_1.html
        :return:
        """
        return re.search(r'(?<=blog\.sina\.com\.cn/s/articlelist_)(?P<sinablog_people_id>[^/\n\r]*)(_0_1\.)', content)

    # csdn
    @staticmethod
    def csdnblog_author(content=''):
        u"""

        :param content: csdn 博主主页地址, http://blog.csdn.net/elton_xiao
        :return: re.match object
        """
        return re.search(r'(?<=blog\.csdn\.net/)(?P<csdnblog_author_id>[^/\n\r]*)', content)

    @staticmethod
    def fix_filename(filename):
        illegal = {
            '\\': '＼',
            '/': '',
            ':': '：',
            '*': '＊',
            '?': '？',
            '<': '《',
            '>': '》',
            '|': '｜',
            '"': '〃',
            '!': '！',
            '\n': '',
            '\r': ''
        }
        for key, value in illegal.items():
            filename = filename.replace(key, value)
        return unicode(filename[:80])

    @staticmethod
    def fix_html(content=''):
        content = content.replace('</br>', '').replace('</img>', '')
        content = content.replace('<br>', '<br/>')
        content = content.replace('<wbr>', '').replace('</wbr>', '<br/>')  # for sinablog
        content = content.replace('href="//link.zhihu.com', 'href="https://link.zhihu.com')  # 修复跳转链接

        # for SinaBlog
        for item in re.findall(r'\<span class="img2"\>.*?\</span\>', content):
            content = content.replace(item, '')
        for item in re.findall(r'\<script\>.*?\</script\>', content, re.S):
            content = content.replace(item, '')
        for item in re.findall(r'height=\".*?\" ', content):     # 因为新浪博客的图片的高,宽是js控制的,不加
            content = content.replace(item, '')                 # 这一段会导致无法匹配
        for item in re.findall(r'width=\".*?\" ', content):
            content = content.replace(item, '')
        for item in re.findall(r'\<cite\>.*?\</cite\>', content):
            content = content.replace(item, '')

        for item in re.findall(r'\<noscript\>.*?\</noscript\>', content, re.S):
            content = content.replace(item, '')
        return content

    @staticmethod
    def detect(command):
        for command_type in Type.type_list:
            result = getattr(Match, command_type)(command)
            if result:
                return command_type
        return 'unknown'

    @staticmethod
    def get_recipe_kind(url):
        u"""

        :param url: one line
        :return: website kind, e.g. 'zhihu', 'jianshu', 'sinablog', 'csdnblog'
        """
        split_url = url.split('#')[0]    # remove comment
        split_url = split_url.split('$')[0]    # the first one determine type
        url_type = Match.detect(split_url)

        recipe_kind = 'Unsupport type'
        for website in Type.website_type:
            if url_type in getattr(Type, website):
                recipe_kind = website
        return recipe_kind
