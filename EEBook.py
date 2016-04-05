# -*- coding: utf-8 -*-
import sys  # 修改默认编码
import os   # 添加系统路径
reload(sys)
base_path = unicode(os.path.abspath('.').decode(sys.stdout.encoding))

# print base_path
sys.path.append(base_path + '/src/lib')

# Python早期版本可以直接用sys.setdefaultencoding('utf-8')，新版本需要先reload一下
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(100000)  # 为BS解析知乎上的长答案增加递归深度限制

from src.main import EEBook

if __name__ == '__main__':
    game = EEBook(recipe_kind='jianshu')
    game.begin()


