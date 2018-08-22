#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import requests

from .base import Base
from match import Match
from elasticsearch import helpers

DAY_TIME_STAMP = os.getenv('DAY_TIME_STAMP')


class ColumnWorker(Base):

    def catch_content(self):
        print("Column worker")
        column_id = Match.column(self.url).group("column_id")
        print("column_id: {}".format(column_id))
        headers = {
          'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36'
        }

        r = requests.get(
            url="https://zhuanlan.zhihu.com/api/columns/ethereum",
            headers=headers
        )
        columns_info = json.loads(r.text)
        print("columns info??? {}".format(columns_info))

        r = requests.get(
            url="https://zhuanlan.zhihu.com/api/columns/ethereum/posts?offset=0&limit=50",
            headers=headers
        )
        article_list = json.loads(r.text)
        bulk_data = list()
        for article in article_list:
            source_doc = {
                "author": article['author']['name'],
                "title": article['title'],
                "dayTimestamp": DAY_TIME_STAMP,
                "content": article["content"]
            }
            bulk_data.append({
                '_index': 'zhihu',
                '_type': self.url + ':content',
                '_id': article['url'],
                '_op_type': 'update',
                '_source': {'doc': source_doc, 'doc_as_upsert': True}
            })
        helpers.bulk(self.es, bulk_data)

        bulk_data.append({
            '_index': 'eebook',
            '_type': 'metadata',
            '_id': self.url,
            '_op_type': 'update',
            '_source': {
                'doc': {
                    'type': 'zhihu',
                    'title': "zhihu_column" + '-' + column_id + '-zhihu2ebook-' + DAY_TIME_STAMP,
                    'book_desp': 'TODO',
                    'created_by': 'knarfeh',
                    'query': {
                        'bool': {
                            'must':[
                                {
                                    "terms": {
                                        "dayTimestamp": [DAY_TIME_STAMP]
                                    }
                                }
                            ]
                        }
                    }
                },
                'doc_as_upsert': True
            }
        })
        helpers.bulk(self.es, bulk_data)