# -*- coding: utf-8 -*-
class Type(object):
    # zhihu
    answer = 'answer'
    question = 'question'
    topic = 'topic'
    collection = 'collection'
    author = 'author'
    column = 'column'
    article = 'article'

    topic_index = 'topic_index'
    collection_index = 'collection_index'

    author_info = 'author_info'
    collection_info = 'collection_info'
    topic_info = 'topic_info'
    column_info = 'column_info'

    zhihu_article_type_list = [
        'article',
        'column',
    ]
    question_answer_type_list = [
        'answer',
        'question'
    ]
    question_type_list = [
        'answer',
        'question',
        'author',
        'collection',
        'topic',
    ]
    zhihu = question_answer_type_list + question_type_list + zhihu_article_type_list

    # sinablog
    sinablog_article = 'sinablog_article'       # 类型是单篇的文章
    sinablog_author = 'sinablog_author'         # 类型是文章的集锦
    sinablog_info = 'sinablog_info'             # 新浪博客的一些基本信息,如作者id

    sinablog = [sinablog_article, sinablog_author, sinablog_info]

    # cnblogs
    cnblogs_article = 'cnblogs_article'
    cnblogs_author = 'cnblogs_author'
    cnblogs_info = 'cnblogs_info'

    cnblogs = [cnblogs_article, cnblogs_author, cnblogs_info]

    # jianshu
    jianshu_article = 'jianshu_article'     # TODO: 单篇文章
    jianshu_author = 'jianshu_author'
    jianshu_info = 'jianshu_info'
    jianshu_collection = 'jianshu_collection'
    jianshu_collection_info = 'jianshu_collection_info'
    jianshu_notebooks = 'jianshu_notebooks'
    jianshu_notebooks_info = 'jianshu_notebooks'

    jianshu = [
        jianshu_article,
        jianshu_author,
        jianshu_info,
        jianshu_collection,
        jianshu_collection_info,
        jianshu_notebooks,
        jianshu_notebooks_info,
    ]

    # csdn
    csdnblog_article = 'csdnblog_article'    # TODO: 单篇文章
    csdnblog_author = 'csdnblog_author'
    csdnblog_info = 'csdnblog_info'
    csdnblog_article_type_list = ['csdn']
    csdnblog = [csdnblog_author, csdnblog_article, csdnblog_info]

    article_type_list = [
        'article',
        'column',
        'sinablog_author',
        'cnblogs_author',
        'jianshu_author',
        'jianshu_collection',
        'jianshu_notebooks',
        'csdnblog_author'
    ]

    # 文章必须放在专栏之前（否则检测类别的时候就一律检测为专栏了） TODO how's that?
    type_list = question_type_list + article_type_list

    info_table = {
        column: column_info,
        author: author_info,
        collection: collection_info,
        topic: topic_info,

        jianshu_collection: jianshu_collection_info,
        jianshu_notebooks: jianshu_notebooks_info,
    }

    website_type = {
        'zhihu': zhihu,
        'jianshu': jianshu,
        'sinablog': sinablog,
        'csdnblog': csdnblog,
        'cnblogs': cnblogs,
    }

    # for --info option
    key_word_to_website_type = {
        'zhihu.com': 'zhihu',
        'jianshu.com': 'jianshu',
        'blog.sina.com.cn': 'sinablog',
        'blog.csdn.net': 'csdnblog'
    }
