from AppKit import NSView, NSColor, NSRectFill, NSScrollView
import vanilla

class DemoView(NSView):
	def drawRect_(self, rect):
		NSColor.redColor().set()
		NSRectFill(self.bounds())

class _DemoView(vanilla.VanillaBaseObject):
	
	nsViewClass = DemoView

	def __init__ (self):
		self._setupView(self.nsViewClass)

class ScrollViewDemo:
	def __init__(self):
		self.w = vanilla.Window((200, 200))
		self.w.view = _DemoView.nsViewClass.alloc().init()
		self.w.view.setFrame_(((0,0),(400,400)))
		self.w.scrollView = vanilla.ScrollView((0,0,0,0),
								self.w.view)
		self.w.open()

if __name__ == "__main__":
    from vanilla.test.testTools import executeVanillaTest
    executeVanillaTest(ScrollViewDemo)