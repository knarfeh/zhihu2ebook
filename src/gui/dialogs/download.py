#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from src.container.books import Book
from src.gui.library import insert_library
from PyQt4.Qt import QDialog, pyqtSignal, QProgressDialog
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import Qt, QThread, QTextCodec
from src.gui.dialogs.ui_download import Ui_Dialog
from src.web.feeds.recipes.model import RecipeModel

from src.tools.path import Path
from src.login import Login
from src.main import EEBook
from src.constants import EPUBSTOR_DIR

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class DownloadDialog(QDialog, Ui_Dialog):
    download = pyqtSignal(object)

    def __init__(self, recipe_model, book_view, parent=None):
        QDialog.__init__(self, parent)

        self.book_view = book_view

        self.setAttribute(Qt.WA_DeleteOnClose)      # 每次关闭对话框删除对话框所占的内存
        self.setupUi(self)

        self.recipe_model = recipe_model

        self.recipe_model.showing_count = 3     # TODO, 改掉这里的硬编码
        self.count_label.setText(
            # NOTE: Number of news sources
            ('%s news sources') % self.recipe_model.showing_count)

        self.download_button.setVisible(False)

        self.initialize_detail_box()
        self.detail_box.setVisible(False)

        self.recipes.setFocus(Qt.OtherFocusReason)
        self.recipes.setModel(recipe_model)
        self.recipes.setAlternatingRowColors(True)

        self.show_password.stateChanged[int].connect(self.set_pw_echo_mode)
        self.download_button.clicked.connect(self.download_button_clicked)
        self.login_button.clicked.connect(self.login_button_clicked)

        QtCore.QObject.connect(self.recipes, QtCore.SIGNAL("clicked (QModelIndex)"), self.row_clicked)

    def set_pw_echo_mode(self, state):
        self.password.setEchoMode(self.password.Normal if state == Qt.Checked else self.password.Password)

    def row_clicked(self, index):
        u"""
        哪一行被选中了
        :return:
        """
        url = str(self.recipes.model().data(index, QtCore.Qt.UserRole))
        print u"哪一行被选中了???" + str(url)

        self.detail_box.setVisible(True)
        if url == 'zhihu':          # TODO: 改掉硬编码, 这里的信息(是否需要登录)应该用xml或数据库记录
            print u"setVisible????"
            self.account.setVisible(True)
            self.blurb.setText('''
            <p>
            <b>%(title)s</b><br>
            %(cb)s %(author)s<br/>
            %(description)s
            </p>
            ''' % dict(title='zhihu', cb='Created by: YaoZeyuan',
                     author='author', description=u'如果需要爬取私人收藏夹,请先登录'))
        elif url == 'jianshu':
            self.account.setVisible(False)
            self.blurb.setText('''
            <p>
            <b>%(title)s</b><br>
            %(cb)s %(author)s<br/>
            %(description)s
            </p>
            ''' % dict(title='jianshu', cb='Created by: Frank',
                     author='author', description=u'https://github.com/knarfeh/jianshu2e-book'))
        elif url == 'SinaBlog':
            self.account.setVisible(False)
            self.blurb.setText('''
            <p>
            <b>%(title)s</b><br>
            %(cb)s %(author)s<br/>
            %(description)s
            </p>
            ''' % dict(title='SinaBlog', cb='Created by: Frank',
                     author='author', description=u'https://github.com/knarfeh/SinaBlog2e-book'))
        return self.recipes.model().data(index, QtCore.Qt.UserRole)

    def initialize_detail_box(self,):
        # self.previous_urn = urn
        self.detail_box.setVisible(True)
        self.download_button.setVisible(True)
        self.detail_box.setCurrentIndex(0)

    def login_button_clicked(self):
        account = str(self.username.text())
        password = str(self.password.text())
        captcha = str(self.captcha.text())

        zhihu = EEBook(recipe_kind='zhihu')    # 目前只有知乎需要登陆 需要将Path初始化

        login = Login(recipe_kind='zhihu')

        if not login.login(account=account, password=password, captcha=captcha):
            click_ok = QtGui.QMessageBox.information(self, u"登陆失败", u"啊哦，登录失败，可能需要输入验证码\n请尝试输入验证码")
            if click_ok:
                login.get_captcha()
                return
        QtGui.QMessageBox.information(self, u"登陆成功", u"恭喜, 登陆成功, 登陆信息已经保存")

    def download_button_clicked(self):

        # url_id = self.recipes.model.data(1, QtCore.Qt.UserRole)    # TODO: 获得选中的recipes
        url_id = str(self.row_clicked(self.recipes.currentIndex()))

        if url_id is None:
            QtGui.QMessageBox.information(self, u"Error", u"选择需要爬取的网站!")
            return

        readlist_content = self.plainTextEdit.toPlainText()

        if readlist_content is None:
            QtGui.QMessageBox.information(self, u"Error", u"请在文本框中输入网址")

        print u"readlist_content???" + str(readlist_content)
        read_list_path = Path.read_list_path
        print u"read_list_path???" + read_list_path

        readList_file = open(read_list_path, 'w')
        readList_file.write(readlist_content)

        readList_file.close()

        game = EEBook(recipe_kind=url_id)

        progress_dlg = QProgressDialog(self)        # TODO: 设置大小, 区域
        progress_dlg.setWindowModality(Qt.WindowModal)
        progress_dlg.setMinimumDuration(5)
        progress_dlg.setWindowTitle(u"请等待")
        progress_dlg.setLabelText(u"制作中...请稍候")
        progress_dlg.setCancelButtonText(u"取消")
        progress_dlg.resize(350, 250)
        progress_dlg.show()
        progress_dlg.setRange(0, 20)

        for i in range(0, 15):
            progress_dlg.setValue(i)
            QThread.msleep(100)

        for i in range(15, 20):
            progress_dlg.setValue(i)
            QThread.msleep(100)
            if progress_dlg.wasCanceled():
                QtGui.QMessageBox.information(self, u"Error", u"电子书制作失败, 请重新操作")
                return

            filename = game.begin()
            progress_dlg.close()
            QtGui.QMessageBox.information(self, u"Error", u"电子书"+str(filename)+u"制作成功")

            file_path = EPUBSTOR_DIR + '/' + filename

            file_name = os.path.basename(str(file_path))
            book_id = file_name.split('.epub')[0]
            book = Book(book_id)
            insert_library(book)

            return


if __name__ == "__main__":
    from PyQt4.Qt import QApplication
    app = QApplication([])
    d = DownloadDialog(RecipeModel())
    d.exec_()
    del app
