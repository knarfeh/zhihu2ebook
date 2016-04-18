# -*- coding: utf-8 -*-
import os
import shutil
import locale


class Path(object):
    u"""
    定义资源,生成的文件等的路径,以及关于路径操作的一些函数
    不能在开头from src.tools.debug import Debug
    """
    base_path = unicode(os.path.abspath('.').decode(locale.getpreferredencoding()))

    config_path = u''     # 根据recipe_kind确定config_path
    db_path = u''         # 根据recipe_kind确定
    sql_path = u''        # 新建数据库的脚本路径
    image_pool_path = u''
    html_pool_path = u''
    result_path = u''
    www_css = u''

    read_list_path = base_path + '/ReadList.txt'

    @staticmethod
    def reset_path():
        Path.chdir(Path.base_path)
        return

    @staticmethod
    def pwd():
        u"""
        输出绝对路径
        :return:
        """
        print os.path.realpath('.')
        return

    @staticmethod
    def get_pwd():
        u"""
        :return: 绝对路径
        """
        path = unicode(os.path.abspath('.').decode(locale.getpreferredencoding()))
        return path

    @staticmethod
    def mkdir(path):
        try:
            os.mkdir(path)
        except OSError:
            from src.tools.debug import Debug
            Debug.logger.debug(u'指定目录 ' + str(path) + str(u' 已存在'))
            pass
        return

    @staticmethod
    def chdir(path):
        u"""
        换路径,如果路径不存在就新建一个
        :param path:
        :return:
        """
        try:
            os.chdir(path)
        except OSError:
            from src.tools.debug import Debug
            Debug.logger.debug(u'指定目录不存在，自动创建之')
            Path.mkdir(path)
            os.chdir(path)
        return

    @staticmethod
    def rmdir(path):
        u"""
        删除整个目录,忽略错误
        :param path:
        :return:
        """
        if path:
            shutil.rmtree(path, ignore_errors=True)
        return

    @staticmethod
    def copy(src, dst):
        if not os.path.exists(src):
            from src.tools.debug import Debug
            Debug.logger.info('{}不存在，自动跳过'.format(src))
            return
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src=src, dst=dst)
        return

    @staticmethod
    def get_filename(src):
        return os.path.basename(src)

    @staticmethod
    def init_base_path(recipe_kind):
        u"""
        初始化路径,不需要实例化 Path 就能执行
        :return:
        """
        Path.base_path = Path.get_pwd()

        Path.www_css = Path.base_path + str(u'/www/css')
        Path.www_image = Path.base_path + str(u'/www/images')

        if recipe_kind == 'jianshu':    # TODO: 用循环解决
            Path.config_path = Path.base_path + str(u'/config/jianshu_config.json')
            Path.db_path = Path.base_path + str(u'/db/jianshu_db_002.sqlite')
            Path.sql_path = Path.base_path + str(u'/db/jianshu.sql')
        elif recipe_kind == 'zhihu':
            Path.config_path = Path.base_path + str(u'/config/zhihu_config.json')
            Path.db_path = Path.base_path + str(u'/db/zhihuDB_173.sqlite')
            Path.sql_path = Path.base_path + str(u'/db/zhihuhelp.sql')
        elif recipe_kind == 'sinablog':
            Path.config_path = Path.base_path + str(u'/config/sinablog_config.json')
            Path.db_path = Path.base_path + str(u'/db/sinablog_db_001.sqlite')
            Path.sql_path = Path.base_path + str(u'/db/sinablog.sql')
        elif recipe_kind == 'csdnblog':
            Path.config_path = Path.base_path + str(u'/config/csdn_config.json')
            Path.db_path = Path.base_path + str(u'/db/csdn_db_001.sqlite')
            Path.sql_path = Path.base_path + str(u'/db/csdnblog.sql')

        Path.html_pool_path = Path.base_path + str(u'/e-books_tmp_source/网页池')
        Path.image_pool_path = Path.base_path + str(u'/e-books_tmp_source/图片池')
        Path.result_path = Path.base_path + str(u'/e-books_produced')
        return

    @staticmethod
    def init_work_directory():
        Path.reset_path()
        Path.mkdir(u'./e-books_tmp_source')
        Path.mkdir(u'./e-books_produced')
        Path.chdir(u'./e-books_tmp_source')
        Path.mkdir(u'./网页池')
        Path.mkdir(u'./图片池')
        Path.reset_path()
        return

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)


