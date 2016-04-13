# -*- coding: utf-8 -*-
from src.container.task import SingleTask, TaskPackage
from src.tools.debug import Debug
from src.tools.match import Match


class UrlParser(object):
    u"""
    通过Parser类，生成任务列表以及查询列表，统一存放于urlInfo中
    task结构
    *   work_list
        *   'answer', 'question', 'author', 'collection', 'topic', 'article', 'column'
            *   按kind分类
            *   分类后为一列表，其内是同类目下所有待抓取的网页链接
            *   抓取时不用考虑抓取顺序，所以可以按类别归并后一块抓取
    *   book_list
        *   'answer', 'question', 'author', 'collection', 'topic', 'article', 'column'
            *   按kind分类
            *   列表中为book信息，每一个book对应一本单独的电子书
            *   应该将同一book_list里的所有book输出到同一本电子书内，这样才符合当时的本意
            *   那就按章节进行区分吧，由RawBook负责进行生成处理
    """
    def __init__(self):
        pass

    @staticmethod
    def get_task(command):
        u"""
        对外的接口, 用来分析指令,
        :param command:   网页的首地址
        :return:
        """
        command = command.split('#')[0]             # remove_comment
        command_list = command.split('$')           # split_command
        Debug.logger.debug(u"[debug]command_list:" + str(command_list))
        raw_task_list = []
        for command in command_list:
            raw_task = UrlParser.parse_command(command)
            if raw_task:
                raw_task_list.append(raw_task)

        task_package = UrlParser.merge_task_list(raw_task_list)
        return task_package

    @staticmethod
    def parse_command(raw_command=''):
        u"""
        分析单条命令并返回待完成的task
        :param raw_command:   网址原始链接, 如:http://blog.sina.com.cn/u/1287694611
        :return: task
        task格式
        *   kind
            *   字符串，见TypeClass.type_list
        *   spider
            *   href
                *   网址原始链接，例http://www.zhihu.com/question/33578941
                *   末尾没有『/』
        *   book
            *   kind
            *   info
            *   question
            *   answer
        """

        def parse_question(command):
            result = Match.question(command)
            question_id = result.group('question_id')
            task = SingleTask()
            task.kind = 'question'

            task.spider.href = 'https://www.zhihu.com/question/{}'.format(question_id)
            task.book.kind = 'question'
            task.book.sql.info = ' question_id = "{}" '.format(question_id)
            task.book.sql.question = 'question_id = "{}"'.format(question_id)
            task.book.sql.answer = 'question_id = "{}"'.format(question_id)
            return task

        def parse_answer(command):
            result = Match.answer(command)
            question_id = result.group('question_id')
            answer_id = result.group('answer_id')
            task = SingleTask()
            task.kind = 'answer'
            task.spider.href = 'https://www.zhihu.com/question/{}/answer/{}'.format(question_id, answer_id)

            task.book.kind = 'answer'
            task.book.sql.info = ' question_id = "{}" '.format(question_id)
            task.book.sql.question = ' question_id = "{}" '.format(question_id)
            task.book.sql.answer = ' question_id = "{}" and answer_id = "{}" '.format(question_id, answer_id)
            return task

        def parse_author(command):
            result = Match.author(command)
            author_id = result.group('author_id')
            task = SingleTask()
            task.kind = 'author'
            task.spider.href = 'https://www.zhihu.com/people/{}'.format(author_id)
            task.book.kind = 'author'
            task.book.sql.info = 'select * from AuthorInfo where author_id = "{}"'.format(author_id)
            task.book.sql.question = 'select * from Question where question_id in (select question_id from \
            Answer where author_id = "{}")'.format(author_id)
            task.book.sql.answer = 'select * from Answer where author_id = "{}"'.format(author_id)
            return task

        def parse_collection(command):
            result = Match.collection(command)
            collection_id = result.group('collection_id')
            task = SingleTask()
            task.kind = 'collection'
            task.spider.href = 'https://www.zhihu.com/collection/{}'.format(collection_id)
            task.book.kind = 'collection'
            task.book.sql.info = 'select * from CollectionInfo where collection_id = "{}"'.format(
                collection_id)
            task.book.sql.question = 'select * from Question where question_id in (select question_id from \
            Answer where href in (select href from CollectionIndex where collection_id = "{}"))'.format(collection_id)
            task.book.sql.answer = 'select * from Answer where href in (select href from \
            CollectionIndex where collection_id = "{}")'.format(collection_id)
            return task

        def parse_topic(command):
            result = Match.topic(command)
            topic_id = result.group('topic_id')
            task = SingleTask()
            task.kind = 'topic'
            task.spider.href = 'https://www.zhihu.com/topic/{}'.format(topic_id)
            task.book.kind = 'topic'
            task.book.sql.info = 'select * from TopicInfo where topic_id = "{}"'.format(topic_id)
            task.book.sql.question = 'select * from Question where question_id in (select question_id from \
            Answer where href in (select href from TopicIndex where topic_id = "{}"))'.format(topic_id)
            task.book.sql.answer = 'select * from Answer where href in (select href from \
            TopicIndex where topic_id = "{}")'.format(topic_id)
            return task

        def parse_article(command):
            result = Match.article(command)
            column_id = result.group('column_id')
            article_id = result.group('article_id')
            task = SingleTask()
            task.kind = 'article'
            task.spider.href = 'https://zhuanlan.zhihu.com/{}/{}'.format(column_id, article_id)
            task.book.kind = 'article'
            task.book.sql.info = ' column_id = "{}" and article_id = "{}" '.format(column_id, article_id)
            task.book.sql.question = ''
            task.book.sql.answer = ' column_id = "{}" and article_id = "{}" '.format(column_id, article_id)
            return task

        def parse_column(command):
            result = Match.column(command)
            column_id = result.group('column_id')
            task = SingleTask()
            task.kind = 'column'
            task.spider.href = 'https://zhuanlan.zhihu.com/{}'.format(column_id)
            task.book.kind = 'column'
            task.book.sql.info = 'select * from ColumnInfo where column_id = "{}" '.format(column_id)
            task.book.sql.question = ''
            task.book.sql.answer = 'select * from Article where column_id = "{}" '.format(column_id)
            return task

        def parse_sinablog_author(command):
            u"""

            :param command: 某个新浪博客博主的首页地址
            :return: task:
            """
            result = Match.sinablog_author(command)
            sinablog_author_id = result.group('sinablog_people_id')
            Debug.logger.debug(u"sinablog_people_id:" + str(sinablog_author_id))
            task = SingleTask()

            task.author_id = sinablog_author_id
            task.kind = 'sinablog_author'
            task.spider.href_article_list = 'http://blog.sina.com.cn/s/articlelist_{}_0_1.html'.\
                format(sinablog_author_id)
            task.spider.href = 'http://blog.sina.com.cn/u/{}'.format(sinablog_author_id)
            task.spider.href_profile = 'http://blog.sina.com.cn/s/profile_{}.html'.format(sinablog_author_id)
            task.book.kind = 'sinablog_author'
            task.book.sql.info_extra = 'creator_id = "{}"'.format(sinablog_author_id)
            task.book.sql.article_extra = 'author_id = "{}"'.format(sinablog_author_id)
            task.book.author_id = sinablog_author_id
            # Debug.logger.debug(u"在parse_sinablog中, task.book.author_id为" + str(task.book.author_id))
            return task

        def parse_jianshu_author(command):
            u"""

            :param command: homepage of someone, e.g. http://www.jianshu.com/users/b1dd2b2c87a8/latest_articles
            :return: task:
            """
            result = Match.jianshu_author(command)
            jianshu_id = result.group('jianshu_id')
            Debug.logger.debug(u"jianshu_id:" + str(jianshu_id))

            task = SingleTask()
            task.author_id = jianshu_id
            task.kind = 'jianshu_author'
            task.spider.href = 'http://www.jianshu.com/users/{}/latest_articles'.format(jianshu_id)
            task.book.kind = 'jianshu_author'
            task.book.sql.info_extra = 'creator_id = "{}"'.format(jianshu_id)
            task.book.sql.article_extra = 'author_id = "{}"'.format(jianshu_id)
            task.book.author_id = jianshu_id
            return task

        def parse_csdnblog_author(command):
            u"""

            :param command: homepage of someone, e.g. http://blog.csdn.net/elton_xiao
            :return: task
            """
            result = Match.csdnblog_author(command)
            csdnblog_author_id = result.group('csdnblog_author_id')
            Debug.logger.debug(u"csdnblog_id:" + str(csdnblog_author_id))

            task = SingleTask()
            task.author_id = csdnblog_author_id
            task.kind = 'csdnblog_author'
            task.spider.href = 'http://blog.csdn.net/{}'.format(csdnblog_author_id)
            task.book.kind = 'csdnblog_author'
            task.book.sql.info_extra = 'creator_id = "{}"'.format(csdnblog_author_id)
            task.book.sql.article_extra = 'author_id = "{}"'.format(csdnblog_author_id)
            task.book.author_id = csdnblog_author_id
            return task

        def parse_error(command):
            if command:
                Debug.logger.info(u"""无法解析记录:{}所属网址类型,请检查后重试。""".format(command))
            return

        parser = {'answer': parse_answer, 'question': parse_question, 'author': parse_author,
                  'collection': parse_collection, 'topic': parse_topic, 'article': parse_article,
                  'column': parse_column,
                  'sinablog_author': parse_sinablog_author,
                  'jianshu_author': parse_jianshu_author,
                  'csdnblog_author': parse_csdnblog_author,
                  'unknown': parse_error, }
        kind = Match.detect(raw_command)

        return parser[kind](raw_command)

    @staticmethod
    def merge_task_list(task_list):
        task_package = TaskPackage()
        for item in task_list:
            task_package.add_task(item)
        return task_package.get_task()
