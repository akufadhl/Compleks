from collections import defaultdict
import base64
import re

thisFont = Glyphs.font
script = "javanese"

letters = []
letter = defaultdict(list)
pasangans = []
pasangan = defaultdict(list)
HasDescenders = set()

for glyph in thisFont.glyphs:
	for layer in glyph.layers:
		if glyph.script == script and int(layer.bounds.origin.y) < -20 and glyph.export == 1:
			#print(glyph.name, int(layer.bounds.origin.y))
			HasDescenders.add(glyph.name)

for glyph in thisFont.glyphs:
	for master in thisFont.masters:
		layer = glyph.layers[master.id]
		for anchor in layer.anchors:
			if glyph.category == "Letter" and glyph.export == 1 and glyph.script == script:
				if anchor.name == 'bottom':
					letters.append(((int(layer.bounds.size.width),glyph.name)))
	
			if glyph.category == "Mark" and glyph.export == 1 and glyph.script == script:
				print(anchor.name)
				if anchor.name == '_bottom':
					width = int(layer.anchors['_bottom'].position.x) - int(layer.bounds.origin.x)
					pasangans.append((width, glyph.name))
#					(int(layer.anchors['_bottom'].position.x) - int(layer.bounds.origin.x)

for value, name in letters:
	letter[value].append(name)
for value, name in pasangans:
	pasangan[value].append(name)

features = set()
min = 30
for v, w in letter.items():
	for x, y in pasangan.items():
		for i, master in enumerate(thisFont.masters):
			if x > v:
				current_name = "".join(w + y)
				name = re.sub('[-_.]', '', current_name)
				value = int((x-v) * 1.2)
				if value > 15:
#					thisFont.masters[master.id].numbers[name.replace('-','')] = value
					thisFont.masters[master.id].setNumberValueValue_forName_(value, name)
					features.add(f"pos @LetterWithBelow [{' '.join(w)}]' [{' '.join(y)}] <${{{name}}} 0 ${{{name}}} 0>;")
#		if x > v:
#			features += "pos @LetterWithBelow [{letter}]' [{pas}] <{value} 0 {value} 0>;\n".format(letter = " ".join(w), pas = " ".join(y),value = x-v)
if len(script) == 0:
	Message("Select Script First")
elif len(features) == 0:
	Message("No Feature Generated")
else:

#	print(letters)

	fea = "lookup contextualKern " + '{\n'+ 'lookupflag UseMarkFilteringSet [' + " ".join([x[1] for x in pasangans]) + '];\n' + '\n'.join([x for x in features]) + '} contextualKern;'
	print(fea)
	if thisFont.classes["LetterWithBelow"]:
		thisFont.classes["LetterWithBelow"].code = " ".join(HasDescenders)
	else:
		thisFont.classes.append(GSClass('LetterWithBelow', " ".join(HasDescenders)))
	if thisFont.features["kern"]:
		thisFont.features["kern"].code = fea
	else:
		thisFont.features.append(GSFeature('kern', fea))
