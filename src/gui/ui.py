#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import subprocess

from PyQt4 import QtGui
from PyQt4.QtGui import (QMainWindow, QDockWidget, QFileDialog, QTableWidgetItem,
                         QAction, QKeySequence, QTableWidget)
from PyQt4.QtCore import Qt, SIGNAL, QSettings, QVariant, QSize, QPoint, QTimer, QFile

from src.tools.debug import Debug
from src.gui.dialogs.scheduler import SchedulerDialog
from src.gui.dialogs.download import DownloadDialog
from src.web.feeds.recipes.model import RecipeModel
from src.gui.library import LibraryTableWidget, insert_library, get_library, remove_from_library
from src.gui.bookview import BookView

from src.container.books import Book
from src.constants import LIBRARY_DIR
from src.resources import qrc_resources

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

print u"在ui2.py中, parentdir是????" + str(parentdir)

reload(sys)
sys.setdefaultencoding('utf-8')


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.filename = ""
        self.read_method_build_in = False    # 若为False, 用系统自带的EPub阅读器打开
        self.library = get_library()

        self.book_view = BookView()
        # ###########actions############################
        self.addBookAction = self.create_action(
            u"添加Epub格式的电子书?????", self.add_book, QKeySequence.Open,
            QtGui.QIcon(":/open3.png"), u"从文件系统中添加"
        )
        # TODO: 切图标
        self.removeAction = self.create_action(
            u"移除Epub格式的电子书", self.remove_book, None,
            QtGui.QIcon(":/remove.png"), u"移除Epub格式电子书"
        )
        # TODO: 切图标
        self.downloadAction = self.create_action(
            u"制作Epub格式电子书", self.make_book, None,
            QtGui.QIcon(":/download.png"), u"制作Epub格式电子书"
        )
        # TODO: 阅读电子书的图标
        self.readAction = self.create_action(
            u"阅读电子书", self.view_book, None,          # TODO
            QtGui.QIcon(":/preview.png"), u"阅读电子书"
        )
        self.toolbarAction = self.create_action(
            "Toggle Toolbar", self.toggle_toolbar
        )
        self.statusbarAction = self.create_action(
            "Toggle statusbar", self.toggle_statusbar
        )
        self.aboutAction = self.create_action(
            "EE-Book Help", None, None, None, None,
        )
        # ###########toolbar############################
        self.toolbar = self.addToolBar("&Options")
        self.add_actions(self.toolbar, (self.addBookAction, self.removeAction,
                         self.downloadAction, self.readAction))
        self.addToolBarBreak()
        self.toolbar.setVisible(True)
        # ###########menubar############################
        self.menu_bar = self.menuBar()
        self.editBook = self.menu_bar.addMenu("&Books")
        self.add_actions(self.editBook, (self.addBookAction, self.removeAction))

        self.view = self.menu_bar.addMenu("&View")
        self.add_actions(self.view, (self.toolbarAction, self.statusbarAction))

        self.helpMenu = self.menu_bar.addMenu("&Help")
        self.add_actions(self.helpMenu, (self.aboutAction, ))

        # Initialize a statusbar for the window
        status = self.statusBar()
        status.setSizeGripEnabled(False)

        self.setGeometry(100, 100, 1030, 800)

        self.library_table = LibraryTableWidget(self.book_view)
        self.library_table.setVisible(True)

        self.setCentralWidget(self.library_table)

        self.setWindowIcon(QtGui.QIcon(":/icon.png"))    # TODO: 切图标

        settings = QSettings()
        size = settings.value("MainWindow/Size", QVariant(QSize(1030, 800))).toSize()
        self.resize(size)

        position = settings.value("MainWindow/Position", QVariant(QPoint(120, 100))).toPoint()
        self.move(position)
        self.restoreState(settings.value("MainWindow/State").toByteArray())

        self.setWindowTitle("EE-Book")
        QTimer.singleShot(0, self.loadInitialFile)
        self.update_library()
        self.create_connections()

    def update_library(self):
        self.library = get_library()

        self.library_table.clear()
        self.library_table.setStyleSheet("selection-background-color: blue")  # 设置选中背景色
        self.library_table.setRowCount(len(self.library['books']))
        self.library_table.setHorizontalHeaderLabels(["Title", "Authors"])

        self.library_table.setAlternatingRowColors(True)
        self.library_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.library_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.library_table.setSelectionMode(QTableWidget.SingleSelection)

        for i, book in enumerate(self.library['books']):
            for j, cell in enumerate((book['title'], book['author'])):
                print str(i) + str(j) + str(cell)
                item = QTableWidgetItem(cell)
                item.setTextAlignment(Qt.AlignCenter)
                # item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEnabled)
                self.library_table.setItem(i, j, item)
        print self.library_table.rowCount()
        print self.library_table.columnCount()
        # for i, book in enumerate(self.library['books']):
        #     print i, book
        self.library_table.resizeColumnsToContents()

    def create_action(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        u"""

        :param text:
        :param slot:
        :param shortcut:
        :param icon:
        :param tip:
        :param checkable:
        :param signal:
        :return:
        """
        action = QAction(text, self)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if icon is not None:
            action.setIcon(icon)
        if tip is not None:
            action.setToolTip(tip)
        if checkable is not None:
            action.setCheckable(checkable)
        return action

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue("MainWindow/Size", QVariant(self.size()))
        settings.setValue("MainWindow/Position", QVariant(self.pos()))
        # settings.setValue("MainWindow/State", QVariant(self.saveState()))

    def loadInitialFile(self):
        settings = QSettings()
        fname = settings.value("LastFile").toString()
        if fname and QFile.exists(fname):
            ok, msg = self.movies.load(fname)
            self.statusBar().showMessage(msg, 5000)

    def toggle_toolbar(self):
        state = self.toolbar.isVisible()
        self.toolbar.setVisible(not state)

    def toggle_statusbar(self):
        state = self.statusbar.isVisible()
        self.statusbar.setVisible(not state)

    def add_book(self):
        u"""
        打开已经在文件系统的电子书到电子书管理器中
        :return:
        """
        # Get filename and show only .epub files    Mac 系统下返回的是native fiel dialog
        book_path = QtGui.QFileDialog.getOpenFileName(self, u'打开Epub格式电子书', ".", "(*.epub)")

        print u"in open_book, book_name is:" + str(book_path)
        print u"in open_book, bookdata path:" + str(LIBRARY_DIR)
        print os.path.dirname(str(book_path))

        if str(book_path) is '':
            # 没有选中电子书
            return

        if os.path.dirname(str(book_path))+os.sep != str(LIBRARY_DIR):
            shutil.copy(str(book_path), LIBRARY_DIR)

        file_name = os.path.basename(str(book_path))
        book_id = file_name.split('.epub')[0]
        book = Book(book_id)
        insert_library(book)
        self.update_library()

        # if self.filename:
        #     TODO 用默认的电子书阅读器打开epub电子书
            # os.system(u'/Applications/calibre.app/Contents/calibre-debug.app/Contents/MacOS/calibre-debug -w "{}"'.
            #           format(self.filename).encode(sys.stdout.encoding))

    def remove_book(self):
        u"""
        移除电子书
        :return:
        """
        # Debug.logger.debug(u"TODO: 移除电子书")
        book_id = self.library['books'][self.library_table.currentRow()]['book_id']
        remove_from_library(book_id)
        # self.library =
        self.update_library()

    def make_book(self):
        u"""
        制作电子书
        :return:
        """
        download = QtGui.QDialog()
        ui = DownloadDialog(RecipeModel())        # TODO: 将任务交给jobs模块,

        ui.exec_()

        del download

    def create_connections(self):
        # self.library_table.connect(self, SIGNAL("itemDoubleClicked(QTableWidgetItem *)"), self.view_book)
        self.library_table.itemDoubleClicked.connect(self.view_book)
        self.library_table.itemClicked.connect(self.row_clicked)
        # self.library_table.connect(self, SIGNAL("itemClicked(QTableWidgetItem *)"), self.row_clicked)

    def row_clicked(self):
        current = self.library_table.currentRow()
        print str(current)
        # TODO
        pass

    def view_book(self):
        u"""
        用电子书阅读器打开选中的电子书
        :return:
        """
        if not self.library_table.isItemSelected(self.library_table.currentItem()):
            QtGui.QMessageBox.information(self, u"Error", u"请选定要打开的电子书")
            return

        book_id = self.library['books'][self.library_table.currentRow()]['book_id']

        print str(book_id)

        if self.read_method_build_in:     # 判断是否用软件内置的EPub阅读器打开
            self.book_view.load_book(book_id)
            self.book_view.show()
        else:
            epub_path = LIBRARY_DIR + '%s.epub' % book_id
            print epub_path     # 进行平台的判断,
            subprocess.call(["open", epub_path])


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


