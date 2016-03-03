#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json


from PyQt4.QtGui import QTableWidget, QTableWidgetItem
from PyQt4.QtCore import Qt, SIGNAL

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

print parentdir

from constants import LIBRARY    # It's ok

# print LIBRARY

def get_library():
    with open(LIBRARY, 'r') as f:
        try:
            library = json.load(f)
        except Exception, e:
            print(e)
            library = {'books': []}
    return library

def insert_library(book):
    lib = get_library()
    book.open()
    lib['books'].append({'book_id': book.book_id, 'title': book.title, 'author': book.author})
    with open(LIBRARY, 'w') as f:
        json.dump(lib, f, indent=4)


class LibraryTableWidget(QTableWidget):

    def __init__(self, book_view, parent=None):
        super(LibraryTableWidget, self).__init__(parent=None)
        self.book_view = book_view

        self.setColumnCount(2)
        self.refresh()
        self.create_connections()

    def refresh(self):
        self.library = get_library()

        self.clear()
        self.setRowCount(len(self.library['books']))
        self.setHorizontalHeaderLabels(['Title', 'Authors'])

        for i, book in enumerate(self.library['books']):
            for j, cell in enumerate((book['title'], book['author'])):
                print str(cell)
                item = QTableWidgetItem(cell)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEnabled)
                self.setItem(i, j, item)

        self.resizeColumnsToContents()

    def create_connections(self):
        self.connect(self, SIGNAL("itemDoubleClicked(QTableWidgetItem *)"), self.view_book)

    def view_book(self):
        book_id = self.library['books'][self.currentRow()]['book_id']
        self.book_view.load_book(book_id)

