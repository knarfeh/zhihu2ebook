#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest

from parser_unit import (is_info, parser)
from correct_dict import checkList


class CsdnblogAuthor(unittest.TestCase):
    def setUp(self):
        self.is_info = is_info
        if self.is_info:
            self.info_list = parser.get_extra_info()
        else:
            self.info_list = parser.get_answer_list()[0]    # TODO

    def failed_tips(self, test_key, kind):
        u"""
        测试失败时，输出提示语句
        :param test_key:
        :param correctValue:
        :return tipString:
        """
        test_key = test_key.encode("utf-8")
        correct_value = checkList[kind][test_key]
        tip_string = u"""\n
        {test_key} parse error
        self.info_dict[{kind}]['{test_key}'] should equal {correct_value}
        but the self.info_dict[{kind}]['{test_key}'] = {errorValue}
                    """.encode("utf-8").format(test_key=test_key, kind=kind,
                                               correct_value=correct_value, errorValue=self.info_list[0][test_key])
        return tip_string

    def test_creator_id(self):
        self.assertEqual(self.info_list[0]["creator_id"],
                         checkList['csdn_blog_author']['creator_id'],
                         self.failed_tips("creator_id", "csdn_blog_author"))

    def test_article_num(self):
        self.assertEqual(self.info_list[0]["article_num"],
                         checkList['csdn_blog_author']['article_num'],
                         self.failed_tips("article_num", "csdn_blog_author"))

    def test_description(self):
        self.assertEqual(self.info_list[0]["description"],
                         checkList['csdn_blog_author']['description'],
                         self.failed_tips("description", "csdn_blog_author"))

    def test_creator_name(self):
        self.assertEqual(self.info_list[0]["creator_name"],
                         checkList['csdn_blog_author']['creator_name'],
                         self.failed_tips("creator_name", "csdn_blog_author"))

if __name__ == '__main__':
    unittest.main()
