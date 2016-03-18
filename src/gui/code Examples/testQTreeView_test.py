#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

HORIZONTAL_HEADERS = (u"website", u"type")

class recipe_class(object):
    '''
    a trivial custom data object
    '''
    def __init__(self, url, type, lang):
        self.url = url
        self.type = type
        self.lang = lang

    def __repr__(self):
        return "website -- %s" % self.url

class TreeItem(object):
    '''
    a python object used to return row/column data, and keep note of
    it's parents and/or children
    '''
    def __init__(self, recipe, header, parentItem):
        self.recipe = recipe
        self.parentItem = parentItem
        self.header = header
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return 2

    def data(self, column):
        if self.recipe == None:
            if column == 0:
                return QtCore.QVariant(self.header)
            if column == 1:
                return QtCore.QVariant("")
        else:
            if column == 0:
                return QtCore.QVariant(self.recipe.url)
            if column == 1:
                return QtCore.QVariant(self.recipe.type)
        return QtCore.QVariant()

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

class treeModel(QtCore.QAbstractItemModel):
    '''
    a model to display a few names, ordered by sex
    '''
    def __init__(self, parent=None):
        super(treeModel, self).__init__(parent)
        self.recipe = []
        for url, type, lang in (("zhihu.com", u"问题, 答案, 专栏", u"Chinese"),
        ("jianshu.com", u"Blogs", u"Chinese"), ("blog.sina.com", u"博客", u"English")):
            recipe = recipe_class(url, type, lang)
            self.recipe.append(recipe)

        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {0: self.rootItem}
        self.setupModelData()

    def columnCount(self, recipe=None):
        if recipe and recipe.isValid():
            return recipe.internalPointer().columnCount()
        else:
            return len(HORIZONTAL_HEADERS)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        item = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return item.data(index.column())
        if role == QtCore.Qt.UserRole:
            if item:
                return item.recipe

        return QtCore.QVariant()

    def headerData(self, column, orientation, role):
        if (orientation == QtCore.Qt.Horizontal and
        role == QtCore.Qt.DisplayRole):
            try:
                return QtCore.QVariant(HORIZONTAL_HEADERS[column])
            except IndexError:
                pass

        return QtCore.QVariant()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        if not childItem:
            return QtCore.QModelIndex()

        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            p_Item = self.rootItem
        else:
            p_Item = parent.internalPointer()
        return p_Item.childCount()

    def setupModelData(self):
        for item in self.recipe:
            type = item.lang

            if not self.parents.has_key(type):
                newparent = TreeItem(None, type, self.rootItem)
                self.rootItem.appendChild(newparent)

                self.parents[type] = newparent

            parentItem = self.parents[type]
            newItem = TreeItem(item, "", parentItem)
            parentItem.appendChild(newItem)

    def searchModel(self, recipe):
        '''
        get the modelIndex for a given appointment
        '''
        def searchNode(node):
            '''
            a function called recursively, looking at all nodes beneath node
            '''
            for child in node.childItems:
                if recipe == child.recipe:
                    index = self.createIndex(child.row(), 0, child)
                    return index

                if child.childCount() > 0:
                    result = searchNode(child)
                    if result:
                        return result

        retarg = searchNode(self.parents[0])
        print retarg
        return retarg

    def find_GivenName(self, url):
        app = None
        for item in self.recipe:
            if item.url == url:
                app = item
                break
        if app != None:
            index = self.searchModel(app)
            return (True, index)
        return (False, None)

if __name__ == "__main__":

    def row_clicked(index):
        '''
        when a row is clicked... show the name
        '''
        print tv.model().data(index, QtCore.Qt.UserRole)

    def but_clicked():
        '''
        when a name button is clicked, I iterate over the model,
        find the person with this name, and set the treeviews current item
        '''
        name = dialog.sender().text()
        print "BUTTON CLICKED:", name
        result, index = model.find_GivenName(name)
        if result:
            if index:
                tv.setCurrentIndex(index)
                return
        tv.clearSelection()

    app = QtGui.QApplication([])

    model = treeModel()
    dialog = QtGui.QDialog()

    dialog.setMinimumSize(300, 150)
    layout = QtGui.QVBoxLayout(dialog)

    tv = QtGui.QTreeView(dialog)
    tv.setModel(model)
    tv.setAlternatingRowColors(True)
    layout.addWidget(tv)

    label = QtGui.QLabel("Search for the following person")
    layout.addWidget(label)

    buts = []
    frame = QtGui.QFrame(dialog)
    layout2 = QtGui.QHBoxLayout(frame)

    for item in model.recipe:
        but = QtGui.QPushButton(item.url, frame)
        buts.append(but)
        layout2.addWidget(but)
        QtCore.QObject.connect(but, QtCore.SIGNAL("clicked()"), but_clicked)

    layout.addWidget(frame)

    but = QtGui.QPushButton("Clear Selection")
    layout.addWidget(but)
    QtCore.QObject.connect(but, QtCore.SIGNAL("clicked()"), tv.clearSelection)

    QtCore.QObject.connect(tv, QtCore.SIGNAL("clicked (QModelIndex)"),
        row_clicked)

    dialog.exec_()

    # app.closeAllWindows()
