#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import requests

from .base import Base
from match import Match
from elasticsearch import helpers
from lxml import html, etree

DAY_TIME_STAMP = os.getenv('DAY_TIME_STAMP')


class ColumnWorker(Base):
    def replace_img_url(self, content):
        utf8_parser = html.HTMLParser(encoding='utf-8')
        tree = html.document_fromstring(str(content), parser=utf8_parser)

        for _pic_link in tree.xpath("//img"):
            href = str(_pic_link.get('src'))
            pic_id, pic_type = href.split('.')
            _pic_link.set('src', "https://pic4.zhimg.com/" + pic_id + "_b." + pic_type)
        replaced_content = etree.tostring(tree, encoding=str)
        return replaced_content

    def catch_content(self):
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
        print("Got column info: {}".format(columns_info["intro"]))

        r = requests.get(
            url="https://zhuanlan.zhihu.com/api/columns/ethereum/posts?offset=0&limit=100",
            headers=headers
        )
        article_list = json.loads(r.text)
        bulk_data = list()
        for article in article_list:
            content = self.replace_img_url(article["content"])
            source_doc = {
                "author": article['author']['name'],
                "title": article['title'],
                "dayTimestamp": DAY_TIME_STAMP,
                "content": str(content)
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
                    'title': "zhihu_column" + '-' + columns_info["name"] + '-zhihu2ebook-' + DAY_TIME_STAMP,
                    'book_desp': columns_info["intro"],
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
