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
import uharfbuzz as hb
import os, vanilla
from AppKit import NSView, NSColor, NSBezierPath, NSWidth, NSHeight, NSAffineTransform, NSScreen, NSViewWidthSizable, NSViewHeightSizable


class CanvasView_view(NSView):

		def init(self):
			self = super(CanvasView_view, self).init()
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
			letters =	self.wrapper._letters
			Binary = self.wrapper._binaryFont
			m = self.wrapper._m
			
			if not letters:
				return

			pathToDraw = None

			try:
				pathToDraw = letters
			except:
				print(traceback.format_exc())
			
			if pathToDraw is None:
				return
			
			try:
				blob = hb.Blob.from_file_path(Binary)
				face = hb.Face(blob)
				font = hb.Font(face)

				buf = hb.Buffer()
				buf.add_str(str(letters))
				buf.guess_segment_properties()
				hb.shape(font, buf)

				infos = buf.glyph_infos
				positions = buf.glyph_positions
				
				xAdv, yAdv = 0, 0
				for info, pos in zip(infos, positions):
					xOff = pos.x_offset
					yOff = pos.y_offset	

					gid = info.codepoint
					glyphname = font.get_glyph_name(gid)
					
					# glyphName = glyphname
					#glyphName = Glyphs.niceGlyphName(glyphname)

					fullpath = NSBezierPath.alloc().init()
					path = f.glyphs[glyphname].layers[m].completeBezierPath

					transform = NSAffineTransform.transform()
					transform.translateXBy_yBy_(xAdv+xOff, yAdv+yOff)
					path.transformUsingAffineTransform_( transform )
					
					
					xAdv += pos.x_advance
					yAdv += pos.y_advance

					transform = NSAffineTransform.transform()
					transform.scaleBy_( scale )
					path.transformUsingAffineTransform_( transform )

					transform = NSAffineTransform.transform()
					transform.translateXBy_yBy_(20, Height/2.2)
					path.transformUsingAffineTransform_(transform)

					fullpath.appendBezierPath_(path)
					NSColor.blackColor().set()
					fullpath.fill()
					print(glyphname, xAdv, yAdv, xOff, yOff)

					
			except:
				print(traceback.format_exc())


class CanvasView(vanilla.VanillaBaseObject):
	nsView = CanvasView_view

	def __init__(self, posSize):
		self._letters = ""
		self._binaryFont = ""
		self._m = None
		self._posSize = posSize

		self._setupView(self.nsView, posSize)
		self._nsObject.wrapper = self

	def redraw(self):
		self._nsObject.setNeedsDisplay_(True)
	
	def _getNSView(self):
		return self._nsObject

class ____PluginClassName____(GeneralPlugin):

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
			self.windowH = 300
			self.windowW = NSScreen.mainScreen().frame().size.width/1.5
			

			self.w = vanilla.Window((self.windowW, self.windowH), "Complex Preview", minSize=((self.windowW/2), self.windowH))
			try:
				self.w.view = CanvasView((0,0,0,0))
				self.w.view._setFrame(((0,0),(self.windowW, self.windowH)))
				self.w.scroll = vanilla.ScrollView((0,0,0,0), self.w.view._getNSView(), hasHorizontalScroller=True, hasVerticalScroller=False, drawsBackground=False)
			except:
				print(traceback.format_exc())
			self.w.textEdit = vanilla.EditText((10, 10, -100, 22), callback = self.textViewer)
			self.w.exportInstance = vanilla.Button((-90, 10, -10, 20), "Export", callback = self.Export_)
			self.w.instanceName = vanilla.TextBox("auto", "Masters :")
			self.w.fontSelector = vanilla.PopUpButton("auto", self.getMasters(), callback = self.textViewer)
			
			rules = [
		    # Horizontal
		    "H:|-[instanceName]-[fontSelector(>=200,<=4000)]-|",
		    "V:[instanceName]-15-|",
		    "V:[fontSelector]-12-|"
		]
			self.w.addAutoPosSizeRules(rules)
			self.w.bind("close", self.close)

			self.w.open()
			self.Export_(None)
			self.changeView_(None)
			Glyphs.addCallback(self.Export_)
			Glyphs.addCallback(self.changeView_, UPDATEINTERFACE)
		except:
			print(traceback.format_exc())

	@objc.python_method
	def __del__(self):
		Glyphs.removeCallback(self.changeView_, UPDATEINTERFACE)
		Glyphs.removeCallback(self.Export_)

	@objc.python_method
	def textViewer(self, sender):
		try:
			self.w.view._letters = self.w.textEdit.get()
			texts = self.w.textEdit.get()
			binaries = self.getBinary()
			self.w.view._m = self.w.fontSelector.get()
			self.w.view._binaryFont = binaries[self.w.fontSelector.get()]
			self.w.view.redraw()
			#self.w.view.process(texts)
		except:
			print(traceback.format_exc())

	def changeView_(self, sender):
		try:
			self.w.view._letters = self.w.textEdit.get()
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
			print(binaryPath)
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

			
			print("Generating ...")

			for idx, m in enumerate(Glyphs.font.masters):
				for instance in Glyphs.font.instances:
					if instance.axes == m.axes:
						instance.generate(FontPath = path,RemoveOverlap = False, AutoHint = False, UseProductionNames = False)
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
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	

