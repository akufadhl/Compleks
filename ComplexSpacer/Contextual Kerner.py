#MenuTitle: Contextual Kerner
# -*- coding: utf-8 -*-

___doc___ = """
Generate a contextual kerning to avoid collision of pasangan with letters that have descenders
"""
import vanilla
from collections import defaultdict


class AvoidColls:

	def __init__(self):
		if Font is None:
			Message("No font selected", "Select a font project!")
			return
		self.w = vanilla.FloatingWindow((200, 70), "Contextual Kerner")
		self.w.textBox = vanilla.TextBox((10, 10, -10, 17), "Script")
		self.w.button = vanilla.Button((10, 40, -10, 20), "Kern It Away 🔥",
						callback= self.KernItAway)
		self.w.script = vanilla.ComboBox((60, 10, -10, 21),
			["javanese", "balinese"])
			
		self.w.open()
		self.w.makeKey()
	
	def KernItAway(self, sender):

		thisFont = Glyphs.font
		script = self.w.script.get()
		
		letters = []
		letter = defaultdict(list)
		pasangans = []
		pasangan = defaultdict(list)
		HasDescenders = ""
		
		for glyph in thisFont.glyphs:
			for layer in glyph.layers:
				if glyph.script == script and int(layer.bounds.origin.y) < -20 and glyph.export == 1:
					#print(glyph.name, int(layer.bounds.origin.y))
					HasDescenders += glyph.name + " "
		
		for glyph in thisFont.glyphs:
			for layer in glyph.layers:
				for anchor in layer.anchors:
					if glyph.category == "Letter" and glyph.export == 1 and glyph.script == script:
						if anchor.name == 'bottom':
							letters.append((int(layer.bounds.size.width),glyph.name))
			
					if glyph.category == "Mark" and glyph.export == 1 and glyph.script == script:
						if anchor.name == '_bottom':
							pasangans.append((int(layer.anchors['_bottom'].position.x) - int(layer.bounds.origin.x), glyph.name))
		
		for value, name in letters:
			letter[value].append(name)
		for value, name in pasangans:
			pasangan[value].append(name)
		
		features = ""
		for v, w in letter.items():
			for x, y in pasangan.items():
				if x > v:
					features += "pos @LetterWithBelow [{letter}]' [{pas}] <{value} 0 {value} 0>;\n".format(letter = " ".join(w), pas = " ".join(y),value = x-v)
		
		if len(script) == 0:
			Message("Select Script First")
		elif len(features) == 0:
			Message("No Feature Generated")
		else:
    
			print(letters)
			print(features)
	
			thisFont.classes.append(GSClass('LetterWithBelow', HasDescenders))
			thisFont.features.append(GSFeature('kern', features))

AvoidColls()