class Stamp(object):
    """
    Simple Stamp
    """
    
    def __init__(self, inName):
        self.stencils = []
        self.name = inName
        
    def AddStencil(self, inStencil):
        self.stencils.append(inStencil)
        
    def StencilCount(self):
        return len(self.stencils)
        
        
class Stencil(object):
    """
    Simple Stencil
    """
    
    def __init__(self, inName):
        self.colliders = []
        self.name = inName
        
    def AddCollider(self, inCollider):
        self.colliders.append(inCollider)
        
    def ColliderCount(self):
        return len(self.colliders)
        
        
        
class Collider(object):
    """
    Simple Collider
    """
    
    def __init__(self, inName):
        self.name = inName