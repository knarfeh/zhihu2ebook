from PyQt4 import QtGui
from stamp_model import StampTreeModel


if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    # Create the stamp model
    stamp_model = StampTreeModel()
    
    # Create the dialog
    dialog = QtGui.QDialog()
    dialog.setMinimumSize(500, 200)
    
    # Add a layout
    layout = QtGui.QVBoxLayout(dialog)
    
    # Add the tree view
    tv = QtGui.QTreeView(dialog)
    tv.setModel(stamp_model)
    tv.setAlternatingRowColors(True)
    
    # To the layout as well
    layout.addWidget(tv)
    
    # Execute
    dialog.exec_()
    
    # Close
    app.closeAllWindows()
    
    
    
    