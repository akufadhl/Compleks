import vanilla
import AppKit

class _CanvasView(AppKit.NSView):

    def drawRect_(self, rect):
        AppKit.NSColor.whiteColor().set()
        AppKit.NSRectFill(self.bounds())

class CanvasView(vanilla.VanillaBaseObject):
    
    nsViewClass = _CanvasView

    def __init__(self, posSize):
        self._setupView(self.nsViewClass, posSize)

class showWindow(object):
    
    def __init__(self):
        self.windowH = 450
        self.windowW = 900


        self.w = vanilla.Window((self.windowW, self.windowH), "Red Block", minSize=(self.windowW, self.windowH+25))
        self.w.textEdit = vanilla.EditText((10, 10, -100, 22))
        self.w.exportInstance = vanilla.Button((-90, 10, -10, 20), "Export")
        #self.w.preview = CanvasView((0,45,0,0))
        self.w.view = CanvasView((0,45,0,self.windowH/1.5))
        self.w.instanceName = vanilla.TextBox((10, self.windowH/1.25, -10, 22), "Instance :")
        self.w.fontSelector = vanilla.PopUpButton((100, self.windowH/1.25, -10, 20), ["Regular","Bold","Italic","Bold Italic"])
        
        self.features = ["blwf","kern","liga","pref"]
        print(self.features)
        
        self.w.featureGroups = vanilla.Group((15, self.windowH/1.15 + 15, -10, 450))
        if len(self.features) != 0:
            for a, feature in enumerate(self.features):

                    x = a*10
                    checkBoxes = vanilla.CheckBox((x*8, 0, 90, 20), feature, callback=self.checkBoxes)
                    setattr(
                            self.w.featureGroups,
                            str(a),
                            checkBoxes
                        )
        else:
            self.w.featureGroups.textBox = vanilla.TextBox((0, 0, -10, 20), "No features found")

        self.w.open()

    def checkBoxes(self, sender):
        print(sender.getPosSize())

if __name__ == "__main__":
    from vanilla.test.testTools import executeVanillaTest
    executeVanillaTest(showWindow)