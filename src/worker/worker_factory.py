#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.worker.zhihu_worker import (QuestionWorker, AuthorWorker, CollectionWorker,
                                     TopicWorker, ColumnWorker)
from src.worker.sinablog_worker import sinablogAuthorWorker
from src.worker.jianshu_worker import JianshuAuthorWorker
from src.worker.csdnblog_worker import csdnAuthorWorker

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

def worker_factory(task):

    # graphviz = GraphvizOutput(output_file='filter_none.png')
    # with PyCallGraph(output=graphviz):
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
    return