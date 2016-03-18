# -*- coding: utf-8 -*-
import sqlite3


from src.tools.path import Path
from src import guide
from src.book import Book
from src.tools.config import Config
from src.tools.debug import Debug
from src.tools.http import Http             # 用于检查更新
from src.tools.db import DB
from login import Login
from src.read_list_parser import ReadListParser
from src.worker import worker_factory
from src.tools.type import Type


class EEBook(object):
    def __init__(self, recipe_kind):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        """
        self.recipe_kind = recipe_kind
        Debug.logger.debug(u"recipe种类是:" + str(recipe_kind))
        Path.init_base_path(recipe_kind)       # 设置路径
        Path.init_work_directory(recipe_kind)  # 创建路径
        self.init_database()        # 初始化数据库
        Config._load()
        return

    @staticmethod
    def init_config(recipe_kind):
        if recipe_kind == 'zhihu':      # TODO: 改掉硬编码
            login = Login(recipe_kind='zhihu')
        else:
            return
        if Config.remember_account:
            print u'检测到有设置文件，是否直接使用之前的设置？(帐号、密码、图片质量)'
            print u'按回车使用之前设置，敲入任意字符后点按回车进行重新设置'
            # if raw_input():
            # login.start()
            # Config.picture_quality = guide.set_picture_quality()
            Config.picture_quality = 1
            # else:
            Http.set_cookie()
        else:
            login.start()
            # Config.picture_quality = guide.set_picture_quality()
            Config.picture_quality = 1

        # 储存设置
        Config._save()
        return

    def begin(self):
        u"""
        程序运行的主函数
        :return: book file 的列表
        """
        Debug.logger.debug(u"#Debug模式#: 不检查更新")
        self.init_config(recipe_kind=self.recipe_kind)
        Debug.logger.info(u"开始读取ReadList.txt的内容")
        bookfiles = []
        with open('./ReadList.txt', 'r') as read_list:
            counter = 1
            for line in read_list:
                line = line.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')  # 移除空白字符
                file_name = self.create_book(line, counter)
                bookfiles.append(file_name)
                counter += 1
        return bookfiles

    @staticmethod
    def create_book(command, counter):
        Path.reset_path()

        Debug.logger.info(u"开始制作第 {} 本电子书".format(counter))
        Debug.logger.info(u"对记录 {} 进行分析".format(command))
        task_package = ReadListParser.get_task(command)  # 分析命令

        if not task_package.is_work_list_empty():
            worker_factory(task_package.work_list)  # 执行抓取程序
            Debug.logger.info(u"网页信息抓取完毕")

        if not task_package.is_book_list_empty():
            Debug.logger.info(u"开始从数据库中生成电子书")
            book = Book(task_package.book_list)
            file_name_set = book.create()

        file_name_set2list = list(file_name_set)
        file_name = '-'.join(file_name_set2list[0:3])

        return file_name

    @staticmethod
    def init_database():
        if Path.is_file(Path.db_path):
            DB.set_conn(sqlite3.connect(Path.db_path))
        else:
            Debug.logger.debug(u"db_path:" + Path.db_path)
            DB.set_conn(sqlite3.connect(Path.db_path))
            # 没有数据库, 新建一个出来
            with open(Path.sql_path) as sql_script:
                DB.cursor.executescript(sql_script.read())
            DB.commit()

    @staticmethod        # TODO 删除这部分????
    def check_update():  # 强制更新
        u"""
            *   功能
                *   检测更新。
                *   若在服务器端检测到新版本，自动打开浏览器进入新版下载页面
                *   网页请求超时或者版本号正确都将自动跳过
            *   输入
                *   无
            *   返回
                *   无
        """
        print u"检查更新。。。"
        try:
            # example:
            # 2016-01-02
            # http://www.dwz.cn/helperupgrade
            content = Http.get_content(u"http://zhihuhelpbyyzy-zhihu.stor.sinaapp.com/ZhihuHelpUpdateTime.txt")
            if not content:
                raise Exception('HttpError')
            time, url = [x.strip() for x in content.split('\n')]
            if time == Config.update_time:
                return
            else:
                print u"发现新版本，\n更新日期:{} ，点按回车进入更新页面".format(time)
                print u'新版本下载地址:' + url
                raw_input()
                import webbrowser
                webbrowser.open_new_tab(url)
        except:
            # 不论发生任何异常均直接返回
            return
