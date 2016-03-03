from PyQt4 import QtGui, QtCore

HORIZONTAL_HEADERS = ("Surname", "Given Name")

class person_class(object):
    '''
    a trivial custom data object
    '''
    def __init__(self, sname, fname, isMale):
        self.sname = sname
        self.fname = fname
        self.isMale = isMale

    def __repr__(self):
        return "PERSON - %s %s"% (self.fname, self.sname)

class TreeItem(object):
    '''
    a python object used to return row/column data, and keep note of
    it's parents and/or children
    '''
    def __init__(self, person, header, parentItem):
        self.person = person
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
        if self.person == None:
            if column == 0:
                return QtCore.QVariant(self.header)
            if column == 1:
                return QtCore.QVariant("")
        else:
            if column == 0:
                return QtCore.QVariant(self.person.sname)
            if column == 1:
                return QtCore.QVariant(self.person.fname)
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
        self.people = []
        for fname, sname, isMale in (("John","Brown", 1),
        ("Fred", "Bloggs", 1), ("Sue", "Smith", 0)):
            person = person_class(sname, fname, isMale)
            self.people.append(person)

        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {0 : self.rootItem}
        self.setupModelData()

    def columnCount(self, parent=None):
        if parent and parent.isValid():
            return parent.internalPointer().columnCount()
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
                return item.person

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
        for person in self.people:
            if person.isMale:
                sex = "MALES"
            else:
                sex = "FEMALES"

            if not self.parents.has_key(sex):
                newparent = TreeItem(None, sex, self.rootItem)
                self.rootItem.appendChild(newparent)

                self.parents[sex] = newparent

            parentItem = self.parents[sex]
            newItem = TreeItem(person, "", parentItem)
            parentItem.appendChild(newItem)

    def searchModel(self, person):
        '''
        get the modelIndex for a given appointment
        '''
        def searchNode(node):
            '''
            a function called recursively, looking at all nodes beneath node
            '''
            for child in node.childItems:
                if person == child.person:
                    index = self.createIndex(child.row(), 0, child)
                    return index

                if child.childCount() > 0:
                    result = searchNode(child)
                    if result:
                        return result

        retarg = searchNode(self.parents[0])
        print retarg
        return retarg

    def find_GivenName(self, fname):
        app = None
        for person in self.people:
            if person.fname == fname:
                app = person
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

    dialog.setMinimumSize(300,150)
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

    for person in model.people:
        but = QtGui.QPushButton(person.fname, frame)
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

    app.closeAllWindows()
