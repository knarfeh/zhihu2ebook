#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt4.Qt import QDialog, pyqtSignal
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import Qt


from src.gui.dialogs.ui_download import Ui_Dialog

from src.web.feeds.recipes.model import RecipeModel

from src.tools.path import Path
from src.login import Login
from src.main import EEBook


class DownloadDialog(QDialog, Ui_Dialog):
    download = pyqtSignal(object)

    def __init__(self, recipe_model, parent=None):
        QDialog.__init__(self, parent)

        self.setAttribute(Qt.WA_DeleteOnClose)      # 每次关闭对话框删除对话框所占的内存
        self.setupUi(self)

        self.recipe_model = recipe_model

        self.recipe_model.showing_count = 3     # TODO, 改掉这里的硬编码
        self.count_label.setText(
            # NOTE: Number of news sources
            ('%s news sources') % self.recipe_model.showing_count)

        self.detail_box.setVisible(False)

        self.recipes.setModel(recipe_model)

        self.download_button.setVisible(False)

        self.initialize_detail_box()

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

        # web_id = self.recipes.model.data(1, QtCore.Qt.UserRole)    # TODO: 获得选中的recipes
        web_id = self.row_clicked(self.recipes.currentIndex())
        print "web_id"

        readlist_content = self.plainTextEdit.toPlainText()

        print web_id
        print readlist_content
        read_list_path = Path.read_list_path
        print read_list_path

        ReadList_object = open(read_list_path, 'w')
        ReadList_object.write(readlist_content)

        ReadList_object.close()

        game = EEBook(recipe_kind='zhihu')
        game.begin()


if __name__ == "__main__":
    from PyQt4.Qt import QApplication
    app = QApplication([])
    d = DownloadDialog(RecipeModel())
    d.exec_()
    del app
