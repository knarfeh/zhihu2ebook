#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt4.QtCore import Qt, SIGNAL

from src.constants import LIBRARY    # It's ok


def get_library():
    with open(LIBRARY, 'r') as f:
        try:
            library = json.load(f)
        except Exception, e:
            print(e)
            library = {'books': []}
    f.close()
    return library


def insert_library(book):
    lib = get_library()
    book.open()
    lib['books'].append({
        'book_id': book.book_id, 'title': book.title, 'author': book.author,
        'tags': book.tags
    })
    with open(LIBRARY, 'w') as f:
        json.dump(lib, f, indent=4)
    f.close()


def remove_from_library(book_id):
    lib = get_library()
    for item in lib['books']:
        if item['book_id'] == book_id:
            lib['books'].remove(item)
    with open(LIBRARY, 'w') as f:
        json.dump(lib, f, indent=4)
    f.close()


class LibraryTableWidget(QTableWidget):

    def __init__(self, book_view, parent=None):
        super(LibraryTableWidget, self).__init__(parent=None)
        self.book_view = book_view

        self.setColumnCount(2)          # TODO: 改掉硬编码?
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)   # 设置为全行选中
        # self.setStyleSheet("QTableWidget::Item{background-color:#FF3EFF}")
        self.setStyleSheet("selection-background-color:blue")  # 设置选中背景色
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setFocus(Qt.MouseFocusReason)
        self.resizeColumnsToContents()
        # selected = None       # TODO: 搜索功能
        # if selected is not None:
        #     selected.setSelected(True)
        # self.setCurrentItem(1)
            # self.scrollToItem(selected)

        self.library = get_library()
        # self.refresh()
        # self.create_connections()

    def refresh(self):

        self.clear()
        self.setStyleSheet("selection-background-color: red")  # 设置选中背景色
        self.setRowCount(len(self.library['books']))
        self.setHorizontalHeaderLabels(['Title', 'Authors', 'Tags'])

        for i, book in enumerate(self.library['books']):
            for j, cell in enumerate((book['title'], book['author'], book['tags'])):
                print str(i) + str(j) + str(cell)
                item = QTableWidgetItem(cell)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, j, item)

        self.resizeColumnsToContents()


