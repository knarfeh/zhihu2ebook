#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from elasticsearch import Elasticsearch
from elasticsearch import helpers

ES_HOST_PORT = os.getenv('ES_HOST_PORT')


class Base(object):
    def __init__(self, client, url):
        self.client = client
        self.url = url
        self.es = Elasticsearch([ES_HOST_PORT])
        self.helpers = helpers
        pass

    def start(self):
        self.catch_content()

    def catch_content(self):
        pass

    def send_data(self):
        pass
