#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Base(object):
    def __init__(self, client, url):
        self.client = client
        self.url = url
        pass

    def start(self):
        self.catch_content()

    def catch_content(self):
        pass

    def send_data(self):
        pass
