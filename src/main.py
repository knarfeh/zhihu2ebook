# -*- coding: utf-8 -*-
import sqlite3


from src.tools.path import Path
from src.book import Book
from src.tools.config import Config
from src.tools.debug import Debug
from src.tools.http import Http             # 用于检查更新
from src.tools.db import DB
from login import Login
from src.url_parser import UrlParser
from src.worker.worker_factory import worker_factory
from src.utils import log


class EEBook(object):
    def __init__(self, recipe_kind='Notset', read_list='ReadList.txt', url=None):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        :param recipe_kind:
        :param read_list_txt_file: default value: ReadList.txt
        :param url:
        :return:
        """
        self.recipe_kind = recipe_kind
        self.read_list = read_list
        self.url = url
        log.warning_log(u"website type: " + str(self.recipe_kind))
        Debug.logger.debug(u"read_list: " + str(self.read_list))
        Debug.logger.debug(u"url: " + str(self.url))

        Debug.logger.debug(u"recipe type:" + str(recipe_kind))
        Path.init_base_path(recipe_kind)        # 设置路径
        Path.init_work_directory()              # 创建路径
        self.init_database()                    # 初始化数据库
        Config._load()
        return

    @staticmethod
    def init_config(recipe_kind):
        if recipe_kind == 'zhihu':      # TODO: 改掉硬编码
            login = Login(recipe_kind='zhihu')
        else:
            return
        # !!!!!发布的时候把Config.remember_account改成false!!!!!,使得第一次需要登录,之后用cookie即可
        # 登陆成功了,自动记录账户
        if Config.remember_account_set:
            Debug.logger.info(u'检测到有设置文件，直接使用之前的设置')
            # if raw_input():
            # login.start()
            # Config.picture_quality = guide.set_picture_quality()
            Config.picture_quality = 1
            # else:
            try:
                Http.set_cookie()   # sinablog, jianshu: DontNeed
            except TypeError:
                print u"没有找到登录成功的cookie记录, 请重新登录"
                login.start()
        else:
            log.warning_log(u"Please login...")
            login.start()
            # Config.picture_quality = guide.set_picture_quality()
            Config.picture_quality = 1
            Config.remember_account_set = True
        # save config
        Config._save()
        return

    def begin(self):
        u"""
        程序运行的主函数
        :return: book file 的列表
        """
        Debug.logger.debug(u"#Debug mode#: don't check update")
        self.init_config(recipe_kind=self.recipe_kind)
        Debug.logger.info(u"Reading ReadList.txt...")
        book_files = []

        if self.url is not None:
            file_name = self.create_book(self.url, 1)
            book_files.append(file_name)
            return book_files

        with open(self.read_list, 'r') as read_list:
            counter = 1
            for line in read_list:
                line = line.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')  # 移除空白字符
                file_name = self.create_book(line, counter)
                book_files.append(file_name)
                counter += 1
        return book_files

    @staticmethod
    def create_book(command, counter):
        Path.reset_path()

        Debug.logger.info(u"开始制作第 {} 本电子书".format(counter))
        Debug.logger.info(u"analysis {} ".format(command))
        task_package = UrlParser.get_task(command)  # 分析命令

        if not task_package.is_work_list_empty():
            worker_factory(task_package.work_list)  # 执行抓取程序
            Debug.logger.info(u"网页信息抓取完毕")

        file_name_set = None
        if not task_package.is_book_list_empty():
            Debug.logger.info(u"开始从数据库中生成电子书")
            book = Book(task_package.book_list)
            file_name_set = book.create()
        if file_name_set is not None:
            file_name_set2list = list(file_name_set)
            file_name = '-'.join(file_name_set2list[0:3])
            return file_name
        return u"no epub file produced"

    @staticmethod
    def init_database():
        if Path.is_file(Path.db_path):
            Debug.logger.debug(u"Connect to the database...")
            Debug.logger.debug(u"db_path: " + str(Path.db_path))
            DB.set_conn(sqlite3.connect(Path.db_path))
        else:
            Debug.logger.debug(u"Create db file...")
            DB.set_conn(sqlite3.connect(Path.db_path))
            with open(Path.sql_path) as sql_script:
                DB.cursor.executescript(sql_script.read())
            DB.commit()
