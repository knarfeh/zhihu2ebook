# -*- coding: utf-8 -*-
# zhihu模块的入口

import sys                       # 修改默认的编码
reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(100000)    # 设置BS解析知乎上的长答案的递归深度限制

from src.main