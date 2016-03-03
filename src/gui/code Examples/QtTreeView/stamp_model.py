from PyQt4 import QtCore
from base_classes import Stamp, Stencil, Collider
from item_classes import RootTreeItem, StampTreeItem, StencilTreeItem, ColliderTreeItem

class StampTreeModel(QtCore.QAbstractItemModel):
    """
    This model is used to display stamp information in a tree view
    """
    
    def __init__(self, inParent = None):
        
        # initialize base class
        super(StampTreeModel, self).__init__(inParent)
        
        # create some data members, these will be set from the outside and trigger a model change
        self.stamps = self.CreateStamps()
        
        # set the root item to add other items to
        self.rootItem = RootTreeItem()
        
        # setup the test
        self.SetupModelData()
        
        
        
    def CreateStamps(self):
        """
        @return: A list of stamps, this is just for testing purposes to create a list of items of
        """
        
        stamps = [Stamp("Colorado"), Stamp("Nirvana"), Stamp("Arkansas"), Stamp("California")]
        for stamp in stamps:
            for si in range(3):
                stencil_name = "%s_stencil_%d" % (stamp.name, si)
                stencil = Stencil(stencil_name)
                for ci in range(2):
                    collider_name = "collider_%d" % ci
                    stencil.AddCollider(Collider(collider_name))
                    
                stamp.AddStencil(stencil)
                
        return stamps
    
    
    
    def SetupModelData(self):
        """
        Creates items for the model the view can work with
        These are created out of the stamps held within the model
        """
        
        for stamp in self.stamps:
            
            # Create a stamp tree item
            stamp_item = StampTreeItem(self.rootItem, stamp)
            
            # for all the stencils attached to the stamp create a stencil
            for stencil in stamp.stencils:
                
                stencil_item = StencilTreeItem(stamp_item, stencil)
                
                for collider in stencil.colliders:
                    
                    # create the collider item
                    collider_item = ColliderTreeItem(stencil_item, collider)
                    
                    # add the collider item to the stencil
                    stencil_item.AddChild(collider_item)
                    
                # add the stencil item to the stamp
                stamp_item.AddChild(stencil_item)
                
            # add the stamp to the root
            self.rootItem.AddChild(stamp_item)
                
                
                
    def index(self, row, column, parentindex): 
        """
        The index is used to access data by the view
        This method overrides the base implementation, needs to be overridden
        @param row: The row to create the index for
        @param column: Not really relevant, the tree item handles this
        @param parent: The parent this index should be created under 
        """
        
        # if the index does not exist, return a default index
        if not self.hasIndex(row, column, parentindex):
            return QtCore.QModelIndex()
        
        # make sure the parent exists, if not assume it's the root
        parent_item = None
        if not parentindex.isValid():
            parent_item = self.rootItem
        else:
            parent_item = parentindex.internalPointer()
            
        # get the child from that parent and create an index for it
        child_item = parent_item.GetChild(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()
        
        
        
    def parent(self, childindex):
        """
        creates an index for a parent based on a child index, and binds the data
        used by the view to get a parent (from a child)
        @param childindex: the index of the child to get the parent from
        """
        
        if not childindex.isValid():
            return QtCore.QModelIndex()
        
        child_item = childindex.internalPointer()
        if not child_item:
            return QtCore.QModelIndex()
        
        parent_item = child_item.GetParent()
        
        if parent_item == self.rootItem:
            return QtCore.QModelIndex()
        
        return self.createIndex(parent_item.Row(), 0, parent_item)
    
    
    
    def rowCount(self, parentindex):
        """
        Returns the amount of rows a parent has
        This comes down to the amount of children associated with the parent
        @param parentindex: the index of the parent
        """
        
        if parentindex.column() > 0:
            return 0
        
        item = None
        if not parentindex.isValid():
            item = self.rootItem
        else:
            item = parentindex.internalPointer()
            
        return item.GetChildCount()
    
    
    
    def columnCount(self, parentindex):
        """
        Amount of columns associated with the parent index
        @param parentindex: the parent index object
        """
        
        if not parentindex.isValid():
            return self.rootItem.ColumnCount()
        
        return parentindex.internalPointer().ColumnCount()
    
    
    
    def data(self, index, role):
        """
        The view calls this to extract data for the row and column associated with the parent object
        @param parentindex: the parentindex to extract the data from
        @param role: the data accessing role the view requests from the model
        """
        
        if not index.isValid():
            return QtCore.QVariant()
        
        # get the item out of the index
        parent_item = index.internalPointer()
        
        # Return the data associated with the column
        if role == QtCore.Qt.DisplayRole:
            return parent_item.Data(index.column())
        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(50,50)
        
        # Otherwise return default
        return QtCore.QVariant()
    
    
    
    def headerData(self, column, orientation, role):
        if (orientation == QtCore.Qt.Horizontal and
        role == QtCore.Qt.DisplayRole):
            try:
                return self.rootItem.Data(column)
            except IndexError:
                pass

        return QtCore.QVariant()