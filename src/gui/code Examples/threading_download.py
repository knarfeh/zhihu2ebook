#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 参数和退出：sys.argv和sys.exit()，常规引入
import sys
# 处理网络连接
import urllib2
# 多线程类
from threading import Thread, RLock
# 任务队列，方便各子线程共用
from Queue import Queue
# 图形界面元素
from PyQt4.QtGui import QApplication, QTreeWidget, QTreeWidgetItem

# 要处理的网址
URLS = [
    'http://baidu.com', 'http://renren.com', 'http://sina.com',
    'http://weibo.com', 'http://youku.com', 'http://csdn.com',
    'http://twitter.com', 'http://youtube.com', 'http://facebook.com',
    'http://github.com', 'http://google.com', 'http://tumblr.com'
]
# 开启的线程数
WORKER_NUM = 5


class DownLoader(QTreeWidget):
    '''下载器，它读入一个网址列表，并使用多线程分别下载对应的网址'''
    def __init__(self, urls=URLS, parent=None):
        super(DownLoader, self).__init__(parent)
        # 传入网址列表
        self.urls = urls
        # 将网址压入队列
        self.queue = Queue()
        for url in self.urls:
            self.queue.put(url)

        # 设置界面大小
        self.resize(400, 400)
        self.setWindowTitle(u'下载器')
        # 设置树为两列
        self.setColumnCount(2)
        # 将第一列设置得宽一些
        self.setColumnWidth(0, 250)
        # 设置表头
        self.setHeaderLabels([u'网址', u'状态'])

        self.items = []
        for url in self.urls:
            # 建立树的一个子元素
            item = QTreeWidgetItem()
            # 将网址填充进第一列
            item.setText(0, url)
            # 元素列表中存进这个元素
            self.items.append(item)
        # 将元素列表中的元素全部加到树中
        self.addTopLevelItems(self.items)
        # 创建一个可重入线程锁，保证线程安全性
        self.lock = RLock()
        # 调用线程函数启动线程
        self.start_workers()

    def start_workers(self):
        # 维护一个线程池，并启动各个线程
        pool = []
        for _ in range(WORKER_NUM):
            # 线程池中加入一个线程
            pool.append(Thread(target=self.download))
            # 确保主进程结束后子线程也退出
            pool[-1].setDaemon(True)
            pool[-1].start()

    def download(self):
        # 从网址队列中取出一个网址，并获得它的序号
        while not self.queue.empty():
            # 获得线程锁，防止其它线程同时对队列进行操作
            self.lock.acquire()
            url = self.queue.get()
            # 释放锁，让其它线程可以从队列中读取网址
            self.lock.release()
            index = self.urls.index(url)
            try:
                # 这里只是打开网页，并没有下载，可以改为自己的函数
                # 连接超时时间设置为10秒，防止无谓的尝试，你懂的
                urllib2.urlopen(url, timeout=10)
                state = '1'
            except:
                state = '0'
            # 将第二列的文字改为下载结果
            self.items[index].setText(1, state)
            # 告诉队列任务结束，准备取出下一个网址
            self.queue.task_done()

def main():
    app = QApplication(sys.argv)
    window = DownLoader()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()