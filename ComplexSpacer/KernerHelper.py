class anchor(object):

    def __init__(self, name: str):
        pass
        
class glyphObject(object):

    def __init__(self, width: int, height: int, category: str, script: str, anchors: anchor):
        self.width = width
        self.height = height
        self.category = category
        self.script = script
        self.anchors = anchors
    
    def __str__(self):
        pass

class kerningPair(object):

    def __init__(self, value: int, Affected: list, Affecting: list, Affector: list = None):
        self.value = value
        self.affected = Affected
        self.affecting = Affecting
        self.affector = Affector
    
    def isContextual():
        return self.affector != None

    def kern():
        pass

    def asFea():
        pass

class pairs(object):

    def __init__(self):
        self.lookup = None
        self.pairs = None