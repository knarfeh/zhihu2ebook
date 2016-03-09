# -*- coding: utf-8 -*-

from src.container.image import ImageContainer
from src.tools.config import Config
from src.tools.db import DB
from src.tools.match import Match
from src.tools.type import Type
from src.tools.debug import Debug


class InitialBook(object):
    class Sql(object):
        def __init__(self):
            self.question = ''
            self.answer = ''
            self.info = ''
            self.article = ''
            self.info_extra = ''
            self.article_extra = ''      # 用来扩展的????
            return

        def get_answer_sql(self):
            return self.answer + Config.sql_extend_answer_filter

    class Epub(object):
        def __init__(self):
            self.article_count = 0
            self.answer_count = 0
            self.agree_count = 0
            self.char_count = 0

            self.title = ''
            self.id = ''
            self.split_index = 0
            self.prefix = ''
            return

    def __init__(self):
        self.kind = ''
        self.author_id = 0                 
        self.sql = InitialBook.Sql()
        self.epub = InitialBook.Epub()
        self.info = {}
        self.article_list = []
        self.page_list = []
        self.prefix = ''
        return

    def catch_data(self):
        u"""
        从数据库中获取数据
        :return:
        """
        self.catch_info()
        self.get_article_list()         # 获取文章所有信息
        if self.kind != Type.SinaBlog and self.kind != Type.jianshu:
            self.__sort()
        return self

    def catch_info(self):
        u"""
        获得博客的信息, 将info作为参数传给set_info
        :return:
        """
        info = {}
        if self.sql.info:
            if self.kind == Type.jianshu:
                info = self.catch_jianshu_book_info()
            elif self.kind == Type.SinaBlog:
                info = self.catch_SinaBlog_book_info()
            elif self.kind in [Type.question, Type.answer]:
                info = self.catch_question_book_info(self.sql.info)
            elif self.kind == Type.article:
                info = self.catch_article_book_info(self.sql.info)
            else:
                info = DB.cursor.execute(self.sql.info).fetchone()
                info = DB.wrap(Type.info_table[self.kind], info)
        self.set_info(info)
        return

    def catch_jianshu_book_info(self):
        u"""

        :param
        :return: info
        """
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.jianshu_info, item) for item in info_list]
        info = {}
        info['creator_name'] = '_'.join([str(item['creator_name']) for item in info_list])  # 可以是多个博客组合在一起
        info['creator_id'] = '_'.join([str(item['creator_id']) for item in info_list])
        return info

    def catch_SinaBlog_book_info(self):
        u"""

        :param
        :return: info
        """
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.SinaBlog_Info, item) for item in info_list]
        info = {}
        info['creator_name'] = '_'.join([str(item['creator_name']) for item in info_list])  # 可以是多个博客组合在一起
        info['creator_id'] = '_'.join([str(item['creator_id']) for item in info_list])
        return info

    def catch_question_book_info(self, sql):
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        # Debug.logger.info(u"第1次的info_list是:" + str(info_list))
        info_list = [DB.wrap(Type.question, item) for item in info_list]
        # Debug.logger.info(u"第2次的info_list是:" + str(info_list))
        info = {}
        info['title'] = '_'.join([str(item['title']) for item in info_list])   # 可以是多个问题, 多个id联系在一起
        info['id'] = '_'.join([str(item['question_id']) for item in info_list])
        # Debug.logger.info(u"catch_question_book_info中的info['id']是什么???" + str(info['id']))
        # Debug.logger.info(u"catch_question_book_info中的info:" + str(info))
        return info

    def catch_article_book_info(self, sql):
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.article, item) for item in info_list]
        info = {}
        info['title'] = '_'.join([str(item['title']) for item in info_list])
        info['id'] = '_'.join([str(item['article_id']) for item in info_list])
        return info

    def set_info(self, info):
        self.info.update(info)
        if self.kind == Type.jianshu:              # 该博客所有的博文
            self.epub.title = u'简书_{}({})'.format(info['creator_name'], info['creator_id'])
            print (u"self.epub.title没有设置???" + str(self.epub.title))
            self.epub.id = info['creator_id']
        elif self.kind == Type.jianshu_article:    # 单篇博文 TODO
            self.epub.title = u'简书博文集锦({})'.format(info['title'])
            self.epub.id = info['id']       # TODO
        elif self.kind == Type.SinaBlog:              # 该博客所有的博文
            self.epub.title = u'新浪博客_{}({})'.format(info['creator_name'], info['creator_id'])
            print (u"self.epub.title没有设置???" + str(self.epub.title))
            self.epub.id = info['creator_id']
        elif self.kind == Type.SinaBlog_Article:    # 新浪单篇博文 TODO
            self.epub.title = u'新浪博客博文集锦({})'.format(info['title'])
            self.epub.id = info['id']       # TODO
        elif self.kind == Type.question:
            self.epub.title = u'知乎问题集锦({})'.format(info['title'])
            self.epub.id = info['id']
        elif self.kind == Type.answer:
            self.epub.title = u'知乎回答集锦({})'.format(info['title'])
            self.epub.id = info['id']
        elif self.kind == Type.article:
            self.epub.title = u'知乎专栏文章集锦({})'.format(info['title'])
            self.epub.id = info['id']

        if self.kind == Type.topic:
            self.epub.title = u'话题_{}({})'.format(info['title'], info['topic_id'])
            self.epub.id = info['topic_id']
        if self.kind == Type.collection:
            self.epub.title = u'收藏夹_{}({})'.format(info['title'], info['collection_id'])
            self.epub.id = info['collection_id']
        if self.kind == Type.author:
            self.epub.title = u'作者_{}({})'.format(info['name'], info['author_id'])
            self.epub.id = info['author_id']
        if self.kind == Type.column:
            self.epub.title = u'专栏_{}({})'.format(info['name'], info['column_id'])
            self.epub.id = info['column_id']
        return

    def get_article_list(self):
        if self.kind in Type.SinaBlog or self.kind in Type.jianshu:
            article_list = self.__get_article_list()
        else:
            article_list = self.__get_question_list()
        self.set_article_list(article_list)
        return

    def __get_question_list(self):
        question_list = [DB.wrap('question', x) for x in DB.get_result_list(self.sql.question)]
        answer_list = [DB.wrap('answer', x) for x in DB.get_result_list(self.sql.get_answer_sql())]

        # Debug.logger.info(u"在__get_question_list中, question_list为:" + str(question_list))
        # Debug.logger.info(u"在__get_question_list中, answer_list为:" + str(answer_list))

        def merge_answer_into_question():
            question_dict = {x['question_id']: {'question': x.copy(), 'answer_list': [], 'agree': 0} for x in
                             question_list}
            for answer in answer_list:
                question_dict[answer['question_id']]['answer_list'].append(answer)
            return question_dict.values()

        def add_property(question):
            agree_count = 0
            char_count = 0
            for answer in question['answer_list']:
                answer['char_count'] = len(answer['content'])
                answer['agree_count'] = answer['agree']
                answer['update_date'] = answer['edit_date']
                agree_count += answer['agree']
                char_count += answer['char_count']
            question['answer_count'] = len(question['answer_list'])
            question['agree_count'] = agree_count
            question['char_count'] = char_count
            return question

        question_list = [add_property(x) for x in merge_answer_into_question() if len(x['answer_list'])]
        return question_list

    def __get_article_list(self):
        def add_property(article):
            article['char_count'] = len(article['content'])
            article['answer_count'] = 1
            if self.kind == Type.SinaBlog or self.kind == Type.jianshu:
                article['agree_count'] = "没有赞同数"     # article['agree']
            else:
                article['agree_count'] = article['agree']

            article['update_date'] = article['publish_date']

            return article

        if self.kind == Type.jianshu:
            article_list = [DB.wrap(Type.jianshu_article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        elif self.kind == Type.SinaBlog:
            article_list = [DB.wrap(Type.SinaBlog_Article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        else:
            article_list = [DB.wrap(Type.article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        article_list = [add_property(x) for x in article_list]
        return article_list

    def set_article_list(self, article_list):
        self.clear_property()
        if self.kind == Type.jianshu:      # jianshu类型
            for article in article_list:
                self.epub.answer_count += article['answer_count']
                self.epub.char_count += article['char_count']
        elif self.kind == Type.SinaBlog:      # SinaBlog类型
            for article in article_list:
                self.epub.answer_count += article['answer_count']
                self.epub.char_count += article['char_count']
        else:                               # zhihu类型
            for article in article_list:
                self.epub.answer_count += article['answer_count']
                self.epub.agree_count += article['agree_count']
                self.epub.char_count += article['char_count']
            self.epub.article_count = len(article_list)         # 所以说, 一个question是一个article
        # Debug.logger.info(u"answer_count和article_count是什么鬼???")
        # Debug.logger.info(u"answer_count:" + str(self.epub.answer_count))
        # Debug.logger.info(u"article_count:" + str(self.epub.article_count))
        self.article_list = article_list
        return

    def clear_property(self):
        self.epub.answer_count = 0
        self.epub.agree_count = 0
        self.epub.char_count = 0
        self.epub.article_count = 0
        return

    def __sort(self):
        if self.kind in Type.article_type_list:
            self.sort_article()
        else:
            self.sort_question()
        return

    def sort_article(self):
        self.article_list.sort(key=lambda x: x[Config.article_order_by], reverse=Config.article_order_by_desc)
        return

    def sort_question(self):
        def sort_answer(answer_list):
            answer_list.sort(key=lambda x: x[Config.answer_order_by], reverse=Config.answer_order_by_desc)
            return

        self.article_list.sort(key=lambda x: x[Config.question_order_by], reverse=Config.question_order_by_desc)
        for item in self.article_list:
            sort_answer(item['answer_list'])
        return


class HtmlBookPackage(object):
    def __init__(self):
        self.book_list = []
        self.image_list = []
        self.image_container = ImageContainer()
        return

    def get_title(self):
        title = '_'.join([book.epub.title for book in self.book_list])
        title = Match.fix_filename(title)  # 移除特殊字符
        return title
