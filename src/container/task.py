# -*- coding: utf-8 -*-

from src.tools.type import Type
from src.container.initialbook import InitialBook


class Spider(object):
    def __init__(self):
        self.href = ''
        return

class SingleTask(object):
    u"""
    任务信息以对象属性方式进行存储
    """

    def __init__(self):
        self.kind = ''
        self.spider = Spider()
        self.book = InitialBook()
        return


class TaskPackage(object):
    u"""
    work_list: kind->single_task.href_index
    book_list: kind->single_task.book
    """
    def __init__(self):
        self.work_list = {}
        self.book_list = {}
        return

    def add_task(self, single_task=SingleTask()):
        if single_task.kind not in self.work_list:
            self.work_list[single_task.kind] = []
        self.work_list[single_task.kind].append(single_task.spider.href)

        if single_task.kind not in self.book_list:
            self.book_list[single_task.kind] = []
        self.book_list[single_task.kind].append(single_task.book)
        return

    def get_task(self):
        if Type.jianshu in self.book_list:
            self.merge_jianshu_article_book_list(Type.jianshu)
        if Type.SinaBlog in self.book_list:
            self.merge_SinaBlog_article_book_list(Type.SinaBlog)
        if Type.answer in self.book_list:
            self.merge_question_book_list(book_type=Type.answer)
        if Type.question in self.book_list:
            self.merge_question_book_list(book_type=Type.question)
        if Type.article in self.book_list:
            self.merge_article_book_list()
        return self

    def merge_jianshu_article_book_list(self, book_type):
        book_list = self.book_list[Type.jianshu]
        book = InitialBook()
        info_extra = [item.sql.info_extra for item in book_list]
        article_extra = [item.sql.article_extra for item in book_list]
        book.kind = book_type
        book.author_id = book_list[0].author_id
        book.sql.info = 'select * from jianshu_info where ({})'.format(' or '.join(info_extra))
        book.sql.article = 'select * from jianshu_article where ({})'.format(' or '.join(article_extra))
        book.sql.answer = 'select * from jianshu_article where ({})'.format(' or '.join(article_extra))
        self.book_list[book_type] = [book]
        return

    def merge_article_book_list(self):
        book_list = self.book_list[Type.article]
        book = InitialBook()
        answer = [item.sql.answer for item in book_list]
        # print u"book_list是???" + str(book_list[0])
        info = [item.sql.info for item in book_list]
        book.kind = Type.article
        book.sql.info = 'select * from Article where ({})'.format(' or '.join(info))
        print u"book.sql.info:????" + str(book.sql.info)
        book.sql.answer = 'select * from Article where ({})'.format(' or '.join(answer))
        self.book_list[Type.article] = [book]
        return

    def merge_question_book_list(self, book_type):
        book_list = self.book_list[book_type]
        book = InitialBook()
        question = [item.sql.question for item in book_list]
        answer = [item.sql.answer for item in book_list]
        info = [item.sql.info for item in book_list]
        book.kind = book_type
        book.sql.info = 'select * from Question where ({})'.format(' or '.join(info))
        book.sql.question = 'select * from Question where ({})'.format(' or '.join(question))
        book.sql.answer = 'select * from Answer where ({})'.format(' or '.join(answer))
        self.book_list[book_type] = [book]
        return

    def merge_SinaBlog_article_book_list(self, book_type):
        book_list = self.book_list[Type.SinaBlog]
        book = InitialBook()
        info_extra = [item.sql.info_extra for item in book_list]
        article_extra = [item.sql.article_extra for item in book_list]
        book.kind = book_type
        book.author_id = book_list[0].author_id       # 这里的len(book_list)比1大怎么办?
        book.sql.info = 'select * from SinaBlog_Info where ({})'.format(' or '.join(info_extra))
        book.sql.article = 'select * from SinaBlog_Article where ({})'.format(' or '.join(article_extra))
        book.sql.answer = 'select * from SinaBlog_Article where ({})'.format(' or '.join(article_extra))
        self.book_list[book_type] = [book]
        return

    def is_work_list_empty(self):
        for kind in Type.type_list:
            if self.work_list.get(kind):
                return False
        return True

    def is_book_list_empty(self):
        for kind in Type.type_list:
            if self.book_list.get(kind):
                return False
        return True
