#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt4.Qt import QDialog, pyqtSignal
from PyQt4 import QtCore

from PyQt4.QtCore import Qt


from src.gui.dialogs.scheduler_ui import Ui_Dialog

from src.web.feeds.recipes.model import RecipeModel

from src.tools.path import Path


class SchedulerDialog(QDialog, Ui_Dialog):
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

        self.download_button = self.buttonBox.addButton(('&Download now'),
                self.buttonBox.ActionRole)   # TODO: set Icon
        self.download_button.setVisible(False)

        self.initialize_detail_box()

        self.recipes.setAlternatingRowColors(True)

        self.download_button.clicked.connect(self.download_button_clicked)

        QtCore.QObject.connect(self.recipes, QtCore.SIGNAL("clicked (QModelIndex)"), self.row_clicked)


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

        from src.main import EEBook     # TODO: 整合其他的网站类型

        game = EEBook(recipe_kind='zhihu')
        game.begin()


if __name__ == "__main__":
    from PyQt4.Qt import QApplication
    app = QApplication([])
    d = SchedulerDialog(RecipeModel())
    d.exec_()
    del app
