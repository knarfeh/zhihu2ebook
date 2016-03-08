# -*- coding: utf-8 -*-
class Type(object):
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

    question_answer_type_list = ['answer', 'question']
    article_type_list = ['article', 'column', ]
    question_type_list = ['answer', 'question', 'author', 'collection', 'topic', ]

    # SinaBlog
    SinaBlog_Article = 'SinaBlog_Article'       # 类型是单篇的文章
    SinaBlog = 'SinaBlog'                       # 类型是文章的集锦

    SinaBlog_Info = 'SinaBlog_Info'             # 新浪博客的一些基本信息,如作者id

    SinaBlog_article_type_list = ['SinaBlog']

    SinaBlog_type_list = ['SinaBlog', ]         # 删除了SinaBlogAuthor

    # jianshu    # TODO, 目前只有latest_articles一种, 还可以写collections, notebook等等
    jianshu_article = 'jianshu_article'     # 类型是单篇的文章   TODO
    jianshu = 'jianshu'                     # 类型是简书文章的集锦

    jianshu_info = 'jianshu_info'

    jianshu_article_type_list = ['jianshu']

    info_table = {
        'jianshu_info': jianshu_info
    }
    jianshu_type_list = [
        'jianshu',
    ]

    # 文章必须放在专栏之前（否则检测类别的时候就一律检测为专栏了） TODO how's that?
    type_list = question_type_list + article_type_list + SinaBlog_type_list + jianshu_type_list

    info_table = {
        column: column_info,
        author: author_info,
        collection: collection_info,
        topic: topic_info,

        'SinaBlog_Info': SinaBlog_Info
    }
    pass
