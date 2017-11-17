#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .base import Base
from match import Match
from elasticsearch import Elasticsearch
from elasticsearch import helpers


class QuestionWorker(Base):
    es = Elasticsearch(['http://192.168.199.121:9200'])

    def catch_content(self):
        question_id = Match.question(self.url).group('question_id')
        question_obj = self.client.question(int(question_id))
        # TODO: hyperlink, pictures, Youku links
        bulk_data = list()
        bulk_data.append({
            '_index': 'zhihu',
            '_type': 'question',
            '_id': question_obj.id,
            '_op_type': 'update',
            '_source': {'doc': question_obj.pure_data, 'doc_as_upsert': True}
        })

        for item in question_obj.answers:
            if item.pure_data['cache'] is not None:
                doc_data = item.pure_data['cache']
            else:
                doc_data = item.pure_data['data']
            doc_data.update({'content': item.content})
            _source_data = {'doc': doc_data, 'doc_as_upsert': True}
            bulk_data.append({
                '_index': 'zhihu',
                '_type': 'answer',
                '_id': item.id,
                '_op_type': 'update',
                '_source': _source_data
            })
        helpers.bulk(self.es, bulk_data)
