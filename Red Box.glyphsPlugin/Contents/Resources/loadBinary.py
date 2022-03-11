import os
from fontTools.ttLib import TTFont
f = Glyphs.font

def getBinaryFont(fontFile):
	path = f.parent.filePath.rsplit('/', 1)[0]
	familyName = f.familyName
	names = [x.name for x in f.instances]
	
	fontNames = []
	
	for name in names:
		fontName = "".join(familyName) + "-" + name
		fontNames.append(fontName)
		
		print(fontName)
		
	print(names,familyName)
	fonts = []
	for fontName in fontNames:
		for fileName in os.listdir(path):
			if fontName in fileName:
				fonts.append(path + "/" + fileName)
	
	print(fonts)
	return fonts

def exportBinary(font):
	if font is None:
		print("No Font Available")
		return
	for instance in font.instances:
		instance.generate(FontPath = font.parent.filePath)

def ftObjects(fontList):
	binaries = []
	for font in fontList:
		binaries.append(TTFont(font))
	print(binaries)
	return binaries
	
fonts = getBinaryFont(f)
binaryFont = ftObjects(fonts)

for font in binaryFont:
	print(font)