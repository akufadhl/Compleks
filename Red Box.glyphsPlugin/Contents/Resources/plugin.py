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
import GlyphsApp.drawingTools as drawBot 
from AppKit import NSView, NSColor, NSBezierPath, NSWidth, NSHeight
import os, vanilla
import uharfbuzz as hb


class CanvasView_view(NSView):

		def init(self):
			self = super(CanvasView_view, self).init()
			self._Text = ""
			self._Binary = ""
			return self

		def process_(self, text):
			self._Text = text
			self._Binary = self.wrapper._binaryFont
			print(self._Binary)

			blob = hb.Blob.from_file_path(self._Binary)
			face = hb.Face(blob)
			font = hb.Font(face)

			buf = hb.Buffer()
			buf.add_str(str(self._Text))
			buf.guess_segment_properties()
			hb.shape(font, buf)

			infos = buf.glyph_infos
			positions = buf.glyph_positions

			for info, pos in zip(infos, positions):
				gid = info.codepoint
				glyphname = font.get_glyph_name(gid)
				xAdv = pos.x_advance
				yAdv = pos.y_advance
				xOff = pos.x_offset
				yOff = pos.y_offset
				print(gid, glyphname, xAdv, yAdv, xOff, yOff)

			print(self._Text)

			self.setNeedsDisplay_(True)

		def drawRect_(self,rect):

			NSColor.whiteColor().set()
			NSBezierPath.fillRect_(rect)
			
			Width = NSWidth(self.frame())
			Height = NSHeight(self.frame())
			
			f = Glyphs.font
			m = f.selectedFontMaster
			scale = 0.444444 / (f.upm / min(Width, Height))
			drawBot.scale(scale)
			drawBot.translate(Width/10 , f.upm/1.5)
			if f is None:
				return

			#Process string and get glyphs info using uharfbuzz

			letters = self.wrapper._letters

			#print(letters)

			#layers = f.selectedLayers
			drawBot.translate(x = 45, y= 45)
			
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
				width = []
				glyphs = []

				for letter in letters:
					width.append(int(f.glyphs[letter].layers[m.id].width))
					glyphs.append(f.glyphs[letter].layers[m.id].completeBezierPath)

				width.insert(0,0)
				glyphToDraw = tuple(zip(width,glyphs))

				advanceX = 0
				for idx, bezier in enumerate(glyphToDraw):
					
					advanceX, y = int(bezier[0]) , 0
					drawBot.translate(advanceX,0)
					drawBot.drawPath(bezier[1])
					NSColor.blackColor().set()
					

			except:
				print(traceback.format_exc())


class CanvasView(vanilla.Group):
		nsViewClass = CanvasView_view

		def __init__(self, posSize):
			self._letters = ""
			self._binaryFont = ""
			self._setupView(self.nsViewClass, posSize)
			self.getNSView().delegate = self
			self._nsObject.wrapper = self

		def redraw(self):
			self._nsObject.setNeedsDisplay_(True)
		
		def process(self, texts):
			self.getNSView().process_(texts)



class ____PluginClassName____(GeneralPlugin):

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
		'en': 'Red Block',
		'de': 'Rot Block',
		})

	@objc.python_method
	def start(self):
		newMenuItem = NSMenuItem(self.name, self.showWindow_)
		Glyphs.menu[EDIT_MENU].append(newMenuItem)

	def showWindow_(self, sender):
		try:
			"""Do something like show a window """
			self.windowH = 250
			self.windowW = 800
			

			self.w = vanilla.Window((self.windowW, self.windowH), "Red Block", minSize=(self.windowW, self.windowH))
			self.w.textEdit = vanilla.EditText((10, 10, -100, 22), callback = self.textViewer)
			self.w.exportInstance = vanilla.Button(((self.windowW-90), 10, -10, 20), "Export")
			#self.w.preview = CanvasView((0,45,0,0))
			self.w.view = CanvasView((0,45,0,0))
			self.w.open()
			self.Export_(None)
			self.changeView_(None)
			Glyphs.addCallback(self.Export_)
			Glyphs.addCallback(self.changeView_, UPDATEINTERFACE)
			print("show Windows")
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
			self.w.view.redraw()
			texts = self.w.textEdit.get()
			self.w.view._binaryFont = self.getBinary()
			self.w.view.process(texts)
		except:
			print(traceback.format_exc())

	def changeView_(self, sender):
		try:
			self.w.view._letters = self.w.textEdit.get()
			self.w.view.redraw()
		except:
			print(traceback.format_exc())
	
	def getBinary(self):
		try:
			#path = os.path.expanduser("~/Library/Application Support/Glyphs 3/Temp")
			path = os.path.expanduser("~/Documents")
			binaryPath = ""
			for instance in Glyphs.font.instances:
				binaryPath += f"{path}/{instance.fontName}.otf"
			
			#print(binaryPath)
			return binaryPath

		except:
			print(traceback.format_exc())

	#@objc.python_method
	def Export_(self, sender):
		try:
			path = os.path.expanduser("~/Documents")
			binaryPath = ""
			print("Generating ...")
			for instance in Glyphs.font.instances:
				instance.generate(FontPath = path)

				print(f"Generated {instance.font.familyName}-{instance.name}.otf")
				binaryPath += f"{path}/{instance.font.familyName}-{instance.name}.otf "
				print(binaryPath)

		except:
			print(traceback.format_exc())

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	

