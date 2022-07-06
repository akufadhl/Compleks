class valueRecord(object):
    
    def __init__(self, xPlace :int, xAdv :int, yPlace :int = 0, yAdv :int = 0):
        self.xPlacement = xPlace
        self.yPlacement = yPlace
        self.xAdvance = xAdv
        self.yAdvance = yAdv
    
    def __str__(self):
        return f"<{self.xPlacement} {self.yPlacement} {self.xAdvance} {self.yAdvance}>"

class kernObject(object):

    def __init__(self):
        self.affecting = list()
        self.affected = list()
        self.affector = list()
        self.kern = valueRecord
        self.script = str()

    def __str__(self):
        affecting = " ".join(str(x) for x in self.affecting)
        affected = " ".join(str(x) for x in self.affected)
        affector = " ".join(str(x) for x in self.affector)
        return f"pos [{affecting}] [{affected}]' [{affector}] {self.kern};"

kern1 = kernObject()
kern1.affecting = ['o-java', 'suku-java']
kern1.affected = ['na-java', 'ma-java']
kern1.affector = ['naMurdaPas-java']
kern1.kernValue = valueRecord(250,250,250,250)

print(kern1)