class DecisionTreeNode():
    # __slots__ = "left","right","depth","H","val","parent","subList"
    __slots__ = "left", "right", "val"
    def __init__(self,val):
        self.left=None
        self.right=None
        self.val=val