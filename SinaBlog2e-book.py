# -*- coding: utf-8 -*-

import sys
reload(sys)
# 修改系统（终端输出）默认的编码，文件格式、处理格式
sys.setdefaultencoding('utf-8')

from src.main import SinaBlog

sina_crawler = SinaBlog()
sina_crawler.start()
