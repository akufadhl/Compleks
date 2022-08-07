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
from GlyphsApp import *
from GlyphsApp.plugins import *
from shaperView import ShaperView
import os, vanilla, objc, traceback
from AppKit import NSScreen


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
				self.w.scroll = vanilla.ScrollView((0,40,0,-60), self.w.view._getNSView(), hasHorizontalScroller=True, hasVerticalScroller=False, drawsBackground=False)
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
			binaries = self.getBinary()
			self.w.view._showBound = self.w.showBounds.get()
			self.w.view._m = self.w.fontSelector.get()
			self.w.view._binaryFont = binaries[self.w.fontSelector.get()]
			if self.w.view._textWidth is not None:
				self.w.view._setFrame(((0,0),((self.w.view._textWidth/3), self.windowH)))
			self.w.view.redraw()
			#self.w.view.process(texts)
		except:
			print(traceback.format_exc())

	def changeView_(self, sender):

		self.w.view._showBound = self.w.showBounds.get()
		if self.w.view._textWidth is not None:
			self.w.view._setFrame(((0,0),((self.w.view._textWidth/3), self.w.scroll.getPosSize()[3])))
		# self.w.view._letters = self.w.textEdit.get()
		# Height = self.w.scroll.getPosSize()[3]
		# if self.w.view._textWidth is not None:
		# 	self.w.view._setFrame(((0,0),((self.w.view._textWidth/2), Height)))
		self.w.view.redraw()
	
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
	

