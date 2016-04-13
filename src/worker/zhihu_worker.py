#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from src.tools.db import DB
from src.tools.http import Http
from src.tools.match import Match

from src.lib.zhihu_parser.author import AuthorParser
from src.lib.zhihu_parser.collection import CollectionParser
from src.lib.zhihu_parser.question import QuestionParser
from src.lib.zhihu_parser.topic import TopicParser
from src.worker.page_worker import PageWorker


class QuestionWorker(PageWorker):
    def parse_content(self, content):
        parser = QuestionParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()
        return


class AuthorWorker(PageWorker):
    def parse_content(self, content):
        parser = AuthorParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url + '/answers?order_by=vote_num')
        if not content:
            return
        self.task_complete_set.add(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}/answers?order_by=vote_num&page={}'.format(target_url, page + 1)
            self.work_set.add(url)
        return

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url + '/about')
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = AuthorParser(content)
        self.info_list.append(parser.get_extra_info())
        return

    def create_save_config(self):
        config = {'Answer': self.answer_list, 'Question': self.question_list, 'AuthorInfo': self.info_list, }
        return config


class CollectionWorker(PageWorker):
    def add_property(self):
        self.collection_index_list = []
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.task_complete_set.add(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}?page={}'.format(target_url, page + 1)
            self.work_set.add(url)
        return

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = CollectionParser(content)
        self.info_list.append(parser.get_extra_info())
        return

    def parse_content(self, content):
        parser = CollectionParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()

        collection_info = parser.get_extra_info()
        self.add_collection_index(collection_info['collection_id'], parser.get_answer_list())
        return

    def add_collection_index(self, collection_id, answer_list):
        for answer in answer_list:
            data = {'href': answer['href'], 'collection_id': collection_id, }
            self.collection_index_list.append(data)
        return

    def create_save_config(self):
        config = {'Answer': self.answer_list, 'Question': self.question_list, 'CollectionInfo': self.info_list,
                  'CollectionIndex': self.collection_index_list, }
        return config


class TopicWorker(PageWorker):
    def add_property(self):
        self.topic_index_list = []
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url + '/top-answers')
        if not content:
            return
        self.task_complete_set.add(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}/top-answers?page={}'.format(target_url, page + 1)
            self.work_set.add(url)
        return

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url + '/top-answers')
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = TopicParser(content)
        self.info_list.append(parser.get_extra_info())
        return

    def parse_content(self, content):
        parser = TopicParser(content)
        self.question_list += parser.get_question_info_list()
        self.answer_list += parser.get_answer_list()

        topic_info = parser.get_extra_info()
        self.add_topic_index(topic_info['topic_id'], parser.get_answer_list())

        return

    def add_topic_index(self, topic_id, answer_list):
        for answer in answer_list:
            data = {'href': answer['href'], 'topic_id': topic_id, }
            self.topic_index_list.append(data)
        return

    def create_save_config(self):
        config = {'Answer': self.answer_list, 'Question': self.question_list, 'TopicInfo': self.info_list,
                  'TopicIndex': self.topic_index_list, }
        return config

    def clear_index(self):
        topic_id_tuple = tuple(set(x['topic_id'] for x in self.topic_index_list))
        sql = 'DELETE  from TopicIndex where topic_id in ({})'.format((' ?,' * len(topic_id_tuple))[:-1])
        DB.cursor.execute(sql, topic_id_tuple)
        DB.commit()
        return


class ColumnWorker(PageWorker):
    u"""
    专栏没有Parser, 因为有api
    """
    def catch_info(self, target_url):
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        result = Match.column(target_url)
        column_id = result.group('column_id')
        content = Http.get_content('https://zhuanlan.zhihu.com/api/columns/' + column_id)
        if not content:
            return
        raw_info = json.loads(content)
        info = dict()
        info['creator_id'] = raw_info['creator']['slug']
        info['creator_hash'] = raw_info['creator']['hash']
        info['creator_sign'] = raw_info['creator']['bio']
        info['creator_name'] = raw_info['creator']['name']
        info['creator_logo'] = raw_info['creator']['avatar']['template'].replace('{id}', raw_info['creator']['avatar'][
            'id']).replace('_{size}', '')

        info['column_id'] = raw_info['slug']
        info['name'] = raw_info['name']
        info['logo'] = raw_info['creator']['avatar']['template'].replace('{id}', raw_info['avatar']['id']).replace(
            '_{size}', '')
        info['article'] = raw_info['postsCount']
        info['follower'] = raw_info['followersCount']
        info['description'] = raw_info['description']
        self.info_list.append(info)
        self.task_complete_set.add(target_url)
        detect_url = 'https://zhuanlan.zhihu.com/api/columns/{}/posts?limit=10&offset='.format(column_id)
        for i in range(info['article'] / 10 + 1):
            self.work_set.add(detect_url + str(i * 10))
        return

    def parse_content(self, content):
        article_list = json.loads(content)
        for info in article_list:
            article = dict()
            article['author_id'] = info['author']['slug']
            article['author_hash'] = info['author']['hash']
            article['author_sign'] = info['author']['bio']
            article['author_name'] = info['author']['name']
            article['author_logo'] = info['author']['avatar']['template'].replace('{id}', info['author']['avatar'][
                'id']).replace('_{size}', '')

            article['column_id'] = info['column']['slug']
            article['name'] = info['column']['name']
            article['article_id'] = info['slug']
            article['href'] = u'https://zhuanlan.zhihu.com/{column_id}/{article_id}'.format(**article)
            article['title'] = info['title']
            article['title_image'] = info['titleImage']
            article['content'] = info['content']
            article['comment'] = info['commentsCount']
            article['agree'] = info['likesCount']
            article['publish_date'] = info['publishedTime'][:10]
            self.answer_list.append(article)
        return

    def create_save_config(self):
        config = {'ColumnInfo': self.info_list, 'Article': self.answer_list}
        return config
