#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.worker.zhihu_worker import (QuestionWorker, AuthorWorker, CollectionWorker,
                                     TopicWorker, ColumnWorker)
from src.worker.sinablog_worker import sinablogAuthorWorker
from src.worker.jianshu_worker import JianshuAuthorWorker
from src.worker.csdnblog_worker import csdnAuthorWorker


def worker_factory(task):
    type_list = {
        'answer': QuestionWorker,
        'question': QuestionWorker,
        'author': AuthorWorker,
        'collection': CollectionWorker,
        'topic': TopicWorker,
        'column': ColumnWorker,
        'article': ColumnWorker,
        'sinablog_author': sinablogAuthorWorker,
        'jianshu_author': JianshuAuthorWorker,
        'csdnblog_author': csdnAuthorWorker
    }
    for key in task:
        worker = type_list[key](task[key])
        worker.start()
        # self.start_catch_info()
        # self.start_create_work_list()
        # self.start_worker()
        # self.save()
    return