# encoding: utf-8

###########################################################################################################
#
#
#	General Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################
from __future__ import division, print_function, unicode_literals
import traceback
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from HBShaper import HBShaping
import os, vanilla
from AppKit import NSView, NSColor, NSBezierPath, NSWidth, NSHeight, NSAffineTransform, NSScreen, NSFrameRect, NSRect, NSMakePoint


class ShaperView_view(NSView):

	def init(self):
		self = super(ShaperView_view, self).init()
		return self
		
	def drawRect_(self,rect):

		try:
			f = Glyphs.font
			NSColor.whiteColor().set()
			NSBezierPath.fillRect_(rect)
			Width = NSWidth(self.frame())
			Height = NSHeight(self.frame())

			scale = 0.38 / (f.upm / min(Width, Height))

			if f is None:
				return
		except:
			print("Error:", traceback.format_exc())

		#Process string and get glyphs info using uharfbuzz
		Binary = self.wrapper._binaryFont
		m = self.wrapper._m
		letters = str(self.wrapper._letters)
		
		if not letters:
			return

		try:
			HB = HBShaping.fromPath(Binary)
			
			xAdv, yAdv = 0, 0
			shaper = HB.shape(letters)
			self.wrapper._textWidth = sum([x.glyphWidth.width for x in shaper])
			print(self.wrapper._textWidth)
			for i in shaper:

				fullpath = NSBezierPath.alloc().init()
				path = f.glyphs[i.glyphname].layers[m].completeBezierPath
				transform = NSAffineTransform.transform()
				transform.translateXBy_yBy_(xAdv + i.xOff, yAdv + i.yOff)
				path.transformUsingAffineTransform_( transform )
				
				xAdv += i.xAd
				yAdv += i.yAd

				transform = NSAffineTransform.transform()
				transform.scaleBy_( scale )
				path.transformUsingAffineTransform_( transform )
				
				transform = NSAffineTransform.transform()
				transform.translateXBy_yBy_(20, Height/2.2)
				path.transformUsingAffineTransform_(transform)
				
				if self.wrapper._showBound: #and (i.glyphname != "space"):
					try:
						bounds = path.bounds()

						rect = NSRect( bounds.origin , bounds.size )
						#fill rect with outline
						NSColor.greenColor().set()
						NSFrameRect(rect)
					
					except:
						pass

				fullpath.appendBezierPath_(path)
				NSColor.blackColor().set()
				fullpath.fill()
				
		except:
			print(traceback.format_exc())
		try:
			ascender = f.glyphs[i.glyphname].layers[m].master.ascender
			capHeight = f.glyphs[i.glyphname].layers[m].master.capHeight
			xHeight = f.glyphs[i.glyphname].layers[m].master.xHeight
			descender = f.glyphs[i.glyphname].layers[m].master.descender
			
			for x in [ascender, capHeight, xHeight, descender, 0]:

				path = NSBezierPath.alloc().init()

				path.moveToPoint_(NSMakePoint(0, x*scale))
				path.lineToPoint_(NSMakePoint(Width, x*scale))
				NSColor.redColor().set()

				transform = NSAffineTransform.transform()
				transform.translateXBy_yBy_(0, Height/2.2)
				path.transformUsingAffineTransform_(transform)

				path.stroke()
		except:
			print(traceback.format_exc())

class ShaperView(vanilla.VanillaBaseObject):
	nsView = ShaperView_view

	def __init__(self, posSize):
		self._letters = ""
		self._binaryFont = ""
		self._m = None
		self._posSize = posSize
		self._showBound = False
		self._textWidth = None
		self._setupView(self.nsView, posSize)
		self._nsObject.wrapper = self

	def redraw(self):
		self._nsObject.setNeedsDisplay_(True)
	
	def _getNSView(self):
		return self._nsObject

class ComplexShaping(GeneralPlugin):

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
		'en': 'Complex Shaping',
		})

	@objc.python_method
	def start(self):
		newMenuItem = NSMenuItem(self.name, self.showWindow_)
		Glyphs.menu[EDIT_MENU].append(newMenuItem)

	def showWindow_(self, sender):
		try:
			"""Do something like show a window """
			self.windowH = 350
			self.windowW = NSScreen.mainScreen().frame().size.width/1.5
			

			self.w = vanilla.Window((self.windowW, self.windowH), "Complex Preview", minSize=((self.windowW/2), self.windowH))
			try:
				self.w.view = ShaperView((0,0,0,0))
				self.w.view._setFrame(((0,0),(self.windowW, self.windowH)))
				self.w.scroll = vanilla.ScrollView((0,0,0,0), self.w.view._getNSView(), hasHorizontalScroller=True, hasVerticalScroller=False, drawsBackground=False)
			except:
				print(traceback.format_exc())
			self.w.textEdit = vanilla.EditText((10, 10, -100, 22), callback = self.textViewer)
			self.w.exportInstance = vanilla.Button((-90, 10, -10, 20), "Export", callback = self.Export_)
			self.w.instanceName = vanilla.TextBox("auto", "Masters :")
			self.w.fontSelector = vanilla.PopUpButton("auto", self.getMasters(), callback = self.textViewer)
			self.w.showBounds = vanilla.CheckBox("auto", "Show BoundingBox", callback = self.textViewer)
			
			rules = [
		    # Horizontal
		    "H:|-[instanceName]-[fontSelector(>=200,<=4000)]-|",
			"H:|-[showBounds]",
		    "V:[instanceName]-15-[showBounds]",
		    "V:[fontSelector]-12-[showBounds]",
			"V:[fontSelector]-[showBounds]-12-|",
		]
			self.w.addAutoPosSizeRules(rules)
			self.w.bind("close", self.close)

			self.w.open()
			self.createNotdef_(None)
			self.Export_(None)
			self.changeView_(None)
			Glyphs.addCallback(self.createNotdef_)
			Glyphs.addCallback(self.Export_)
			Glyphs.addCallback(self.changeView_, UPDATEINTERFACE)
			
		except:
			print(traceback.format_exc())

	@objc.python_method
	def __del__(self):
		Glyphs.removeCallback(self.changeView_, UPDATEINTERFACE)
		Glyphs.removeCallback(self.Export_)
		Glyphs.removeCallback(self.createNotdef_)

	@objc.python_method
	def textViewer(self, sender):
		try:
			self.w.view._letters = self.w.textEdit.get()
			texts = self.w.textEdit.get()
			binaries = self.getBinary()
			self.w.view._showBound = self.w.showBounds.get()
			self.w.view._m = self.w.fontSelector.get()
			self.w.view._binaryFont = binaries[self.w.fontSelector.get()]
			if self.w.view._textWidth is not None:
				self.w.view._setFrame(((0,0),((self.w.view._textWidth/2), self.windowH)))
			self.w.view.redraw()
			#self.w.view.process(texts)
		except:
			print(traceback.format_exc())

	def changeView_(self, sender):
		try:
			self.w.view._showBound = self.w.showBounds.get()
			self.w.view._letters = self.w.textEdit.get()
			self.w.view._setFrame(((0,0),(self.w.view._textWidth, self.windowH)))
			self.w.view.redraw()
		except:
			print(traceback.format_exc())
	
	def getMasters(self):
		try:
			masters = []

			for m in Glyphs.font.masters:
				for instance in Glyphs.font.instances:
					if instance.axes == m.axes:
						masters.append(m.name)
			
			return masters
		except:
			print(traceback.format_exc())

	def getBinary(self):
		try:
			#path = os.path.expanduser("~/Library/Application Support/Glyphs 3/Temp")
			path = os.path.expanduser("~/Documents")
			binaryPath = {}

			for idx, m in enumerate(Glyphs.font.masters):
				for instance in Glyphs.font.instances:
					if instance.axes == m.axes:
						binaryPath[idx] = path + "/" + instance.fontName + ".otf"
			return binaryPath

		except:
			print(traceback.format_exc())

	#@objc.python_method
	def Export_(self, sender):
		try:
			path = os.path.expanduser("~/Documents")

			print("Compiling Features..")
			Glyphs.font.compileFeatures()
			print("Features Compiled")

			

			for idx, m in enumerate(Glyphs.font.masters):
				for instance in Glyphs.font.instances:
					if instance.axes == m.axes:
						instance.generate(Format = OTF, FontPath = path, RemoveOverlap = False, AutoHint = False, UseProductionNames = False)
			
			print("Files Generated")
			self.w.view.redraw()
		except:
			print(traceback.format_exc())
	@objc.python_method
	def close(self, sender):
		try:

			print("Removing File...", sender)

			#path = os.path.expanduser("~/Library/Application Support/Glyphs 3/Temp")
			path = os.path.expanduser("~/Documents")
			for idx, m in enumerate(Glyphs.font.masters):
				for instance in Glyphs.font.instances:
					if instance.axes == m.axes:
						os.remove( path + "/" + instance.fontName + ".otf")
			
			print("File Removed", sender)

		except:
			print(traceback.format_exc())
	
	@objc.python_method
	def createNotdef_(self, sender):
		try:

			font = Glyphs.font
			notdef = font.glyphs['.notdef']
			
			if notdef:
				print("notdef already exist")
				return

			elif not notdef:
				newGlyph = GSGlyph()
				newGlyph.name = '.notdef'
				font.glyphs.append(newGlyph)
				newGlyph.updateGlyphInfo()
				self.drawSquare()
			
		except:
			print(traceback.format_exc())
		
	def drawSquare(self):
		
		square = ((89,-135), (531, -135), (531,752), (89, 752))

		for layer in Glyphs.font.glyphs['.notdef'].layers:
			if layer.isMasterLayer:
				pen = layer.getPen()
				pen.moveTo(square[0])
				for segment in square[1:]:
					pen.lineTo(segment)
				pen.closePath()
				pen.endPath()
			layer.leftMetricsKey = '=45'
			layer.rightMetricsKey = '=|'
			layer.syncMetrics()

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
