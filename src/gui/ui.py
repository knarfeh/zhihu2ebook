# -*- coding: utf-8 -*-

import sys
import os
import shutil

from PyQt4 import QtGui
from PyQt4.QtGui import (QMainWindow, QDockWidget, QFileDialog)
from PyQt4.QtCore import Qt

from src.tools.debug import Debug
from src.gui.dialogs.scheduler import SchedulerDialog
from src.web.feeds.recipes.model import RecipeModel
from src.gui.library import LibraryTableWidget, insert_library
from src.gui.bookview import BookView

from src.container.books import Book



from src.resources import qrc_resources

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

print parentdir

from constants import LIBRARY_DIR     # It's ok


reload(sys)
sys.setdefaultencoding('utf-8')


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.filename = ""

        self.init_UI()


    def init_UI(self):
        self.init_toolbar()
        self.init_menubar()
        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        self.setGeometry(100, 100, 1030, 800)

        self.create_layout()

        self.setWindowTitle("EE-Book")
        self.setWindowIcon(QtGui.QIcon(":/icon.png"))    # TODO: 切图标

    def create_layout(self):
        self.bookview = BookView()
        self.setCentralWidget(self.bookview)
        self.create_library_dock()

    def create_library_dock(self):
        if getattr(self, 'dock', None):
            self.dock.show()
            return
        self.dock = QDockWidget("library", self)
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.library = LibraryTableWidget(self.bookview)
        self.dock.setWidget(self.library)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)


    def init_toolbar(self):
        self.addBookAction = QtGui.QAction(QtGui.QIcon(":/open3.png"), u"添加epub格式的电子书", self)
        self.addBookAction.setStatusTip(u"添加Epub格式的电子书")
        self.addBookAction.setShortcut("Ctrl+o")
        self.addBookAction.triggered.connect(self.add_book)

        # TODO: remove的图标有点问题
        self.removeAction = QtGui.QAction(QtGui.QIcon(":/remove.png"), u"移除Epub格式电子书", self)
        self.removeAction.setStatusTip(u"移除Epub格式的电子书")
        self.removeAction.setShortcut("Ctrl+r")    # TODO
        self.removeAction.triggered.connect(self.remove_book)

        # TODO: 切图标
        self.downloadAction = QtGui.QAction(QtGui.QIcon(":/download.png"), u"制作Epub格式电子书", self)
        self.downloadAction.setStatusTip(u"制作Epub格式电子书")
        self.downloadAction.setShortcut("Ctrl+d")     # TODO
        self.downloadAction.triggered.connect(self.make_book)

        # TODO: 阅读电子书的图标
        self.readAction = QtGui.QAction(QtGui.QIcon(":/preview.png"), u"阅读电子书", self)
        self.readAction.setStatusTip(u"阅读Epub格式电子书")
        self.downloadAction.setShortcut("Ctrl+r")      # TODO
        self.readAction.triggered.connect(self.read)


        self.toolbar = self.addToolBar("Options")
        self.toolbar.addAction(self.addBookAction)
        self.toolbar.addAction(self.removeAction)
        self.toolbar.addAction(self.downloadAction)
        self.toolbar.addAction(self.readAction)

        self.addToolBarBreak()

    def init_menubar(self):
        menubar = self.menuBar()

        editBook = menubar.addMenu("Add & remove books")
        view = menubar.addMenu("view")
        helpMenu = menubar.addMenu("&Help")


        editBook.addAction(self.addBookAction)
        editBook.addAction(self.removeAction)

        toolbarAction = QtGui.QAction("Toggle Toolbar", self)
        toolbarAction.triggered.connect(self.toggle_toolbar)

        statusbarAction = QtGui.QAction("Toggle statusbar", self)
        statusbarAction.triggered.connect(self.toggle_statusbar)

        # TODO: Q: 必须有关键字Help???
        aboutAction = QtGui.QAction("EE-Book Help", self)   # TODO: 写一个create_action的模块

        view.addAction(toolbarAction)
        view.addAction(statusbarAction)

        helpMenu.addAction(aboutAction)

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

        if os.path.dirname(str(book_path))+os.sep != str(LIBRARY_DIR):
            shutil.copy(str(book_path), LIBRARY_DIR)

        file_name = os.path.basename(str(book_path))
        print "file_name?" + file_name
        book_id = file_name.split('.epub')[0]
        book = Book(book_id)
        insert_library(book)
        self.library.refresh()

        # if self.filename:
        #     TODO 用默认的电子书阅读器打开epub电子书
            # os.system(u'/Applications/calibre.app/Contents/calibre-debug.app/Contents/MacOS/calibre-debug -w "{}"'.
            #           format(self.filename).encode(sys.stdout.encoding))

    def read(self):
        u"""
        用电子书阅读器打开选中的电子书
        :return:
        """
        print u"用电子书阅读器打开选中的电子书"

    def remove_book(self):     # 管理电子书的模块3天后再写
        u"""
        移除电子书
        :return:
        """
        # Debug.logger.debug(u"TODO: 移除电子书")
        print u"TODO: 移除电子书"
        # test_dialog = QtGui.QDialog()
        # ui = Ui_Dialog()
        # ui.setupUi(test_dialog)
        # test_dialog.show()
        # test_dialog.exec_()

    def make_book(self):
        u"""
        制作电子书
        :return:
        """
        Schedule = QtGui.QDialog()
        ui = SchedulerDialog(RecipeModel())        # TODO: 将任务交给jobs模块,

        ui.exec_()

        del Schedule

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


