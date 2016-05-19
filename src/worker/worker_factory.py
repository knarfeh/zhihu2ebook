#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.worker.zhihu_worker import (QuestionWorker, AuthorWorker, CollectionWorker,
                                     TopicWorker, ColumnWorker)
from src.worker.sinablog_worker import sinablogAuthorWorker
from src.worker.jianshu_worker import JianshuAuthorWorker
from src.worker.jianshu_worker import JianshuCollectionWorker
from src.worker.jianshu_worker import JianshuNotebooksWorker
from src.worker.csdnblog_worker import csdnAuthorWorker
from src.worker.cnblogs_worker import CnblogsAuthorWorker
from src.worker.yiibai_worker import YiibaiWorker
from src.worker.talkpython_worker import TalkPythonWorker


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
        'cnblogs_author': CnblogsAuthorWorker,
        'jianshu_author': JianshuAuthorWorker,
        'jianshu_collection': JianshuCollectionWorker,
        'jianshu_notebooks': JianshuNotebooksWorker,
        'csdnblog_author': csdnAuthorWorker,
        'yiibai': YiibaiWorker,
        'talkpython': TalkPythonWorker,
    }
    for key in task:
        worker = type_list[key](task[key])
        worker.start()
    return