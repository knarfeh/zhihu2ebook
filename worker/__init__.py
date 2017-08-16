#!/usr/bin/env python
# -*- coding: utf-8 -*-


from common import str2bool
from .question import QuestionWorker


def worker_factory(_client, _type, _url):
    type_list = {
        'question': QuestionWorker,
    }
    worker = type_list[_type](_client, _url)
    worker.start()
    return
