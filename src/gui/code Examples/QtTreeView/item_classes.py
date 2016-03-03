class BaseTreeItem(object):
    """
    an item that can be used to populate a tree view, knowing it's place in the model
    """
    
    def __init__(self, inParentItem):
        """
        Derive specific tree item objects from this guy
        Override the specific methods that the model needs
        @param inParentItem: The parent of a type BaseTreeItem
        """
        
        self.parent = inParentItem
        self.children = []
        
    def AddChild(self, inChild):
        """
        @param inChild: The child to add, of a type BaseTreeItem
        """
        
        self.children.append(inChild)
    
    def GetChildCount(self):
        """
        @return: The number of children this item holds
        """
        
        return len(self.children)
        
    def GetChild(self, row):
        """
        @return: The child living at that specific row index (starting from 0)
        """
        
        return self.children[row]
    
    def GetParent(self):
        """
        @return: simply returns the parent for this item, of a type BaseTreeItem
        """
        
        return self.parent
    
    def ColumnCount(self):
        """
        @return: The amount of columns this tree item has
        needs to be implemented by derived classes
        """
        
        raise Exception("Column Count Not Specified!!")
    
    def Data(self, inColumn):
        """
        @return: Returns the data to display!
        Needs the be implemented by derived classes
        """
        
        raise Exception("Data gather method not implemented!")
    
    def Parent(self):
        """
        @return: the BaseTreeItem parent object
        """
        
        return self.parent
    
    def Row(self):
        """
        @return the row this item resides on (int)
        """
        
        if self.parent:
            return self.parent.children.index(self)
        return 0
    
    
    
class StampTreeItem(BaseTreeItem):
    """
    represents a stamp item
    """
    
    def __init__(self, inParent, inStamp):
        """
        Initializes itself with a BaseTreeItem derived object and a stamp
        @param inParent: A Root Tree Item
        @param inStamp:  A Stamp object
        """
        
        super(StampTreeItem, self).__init__(inParent)
        self.stamp = inStamp
        
    def ColumnCount(self):
        """
        Holds only 1 column
        """
        return 1
    
    def Data(self, inColumn):
        """
        @return: The name of the stamp
        """
        
        if inColumn == 0:
            return self.stamp.name
        return ""
    

    
class RootTreeItem(BaseTreeItem):
    """
    Represents the root of the tree
    """
    
    def __init__(self):
        """
        The root has no parents and no data it needs to retrieve info from
        """
        super(RootTreeItem, self).__init__(None)
        
    def ColumnCount(self):
        """
        Holds only 1 column
        """    
        return 1
    
    def Data(self, inColumn):
        """
        The root doesn't get displayed and for that reason has no meaning
        But because I like providing meaning, i give it a return value
        """
        if inColumn == 0:
            return "All Stamps"
        return ""
    

    
class StencilTreeItem(BaseTreeItem):
    """
    Represents a stencil in the tree
    """
    
    def __init__(self, inParent, inStencil):
        """
        Initializes itself with a BaseTreeItem derived object and a stencil
        @param inParent: The node to parent to, most likely a stamp
        @param inStencil: The stencil as data object
        """
        
        super(StencilTreeItem, self).__init__(inParent)
        self.stencil = inStencil
    
    def ColumnCount(self):
        """
        Holds only 1 column
        """
        return 1
        
    def Data(self, inColumn):
        """
        @return: The name of the stencil
        """
        
        if inColumn == 0:
            return self.stencil.name
        return ""
    

    
class ColliderTreeItem(BaseTreeItem):
    """
    Represents a collider in the tree
    """
    
    def __init__(self, inParent, inCollider):
        """
        Initializes itself with a BaseTreeItem
        @param inParent: The node to parent to
        @param inCollider: The collider data
        """
        super(ColliderTreeItem, self).__init__(inParent)
        self.collider = inCollider
        
    def ColumnCount(self):
        """
        Holds only 1 column
        """
        return 1
    
    def Data(self, inColumn):
        """
        @return: The name of the column
        """
        
        if inColumn == 0:
            return self.collider.name
        return ""