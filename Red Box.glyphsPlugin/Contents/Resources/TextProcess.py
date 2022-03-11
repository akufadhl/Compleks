import uharfbuzz as hb
from fontTools.pens.cocoaPen import CocoaPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Offset

class GlyphInfo(object):
    
    def __init__(self, glyph=None, xPlacement=0, yPlacement=0, xAdvance=0, yAdvance=0):
        self.glyph = glyph
        self.advanceWidth = 0
        self.advanceHeight = 0
        if glyph is not None:
            self.advanceWidth = glyph.width
            self.advanceHeight = glyph.height
        self.xPlacement = 0
        self.yPlacement = 0
        self.xAdvance = xAdvance - self.advanceWidth
        self.yAdvance = yAdvance - self.AdvanceHeight
        

class stringProcess(object):
    
    def __init__(self):
        self.texts = "ꦏꦿꦁꦱꦺꦏ꧀ꦏ" #get text from vanilla window
        self.font_path = "/Users/fadhlschriftlabor/Desktop/Tuladhajavanese-Regular.otf"
        self.typo_ascender = 0#font.ascender
        self.typo_descender = 0#font.descender
        self.features = {"kern": True, "liga": True}
        self.direction = 'ltr'
        #vhea_ascender = None, vhea_descender = None, contain False,        

    def harfingz(self, text, font_path, typo_ascender, typo_descender, features=None, direction="ltr"):

            blob = hb.Blob.from_file_path(font_path)
            face = hb.Face(blob)
            font = hb.Font(face)
            buf = hb.Buffer()
            buf.direction = direction
            buf.add_str(text)
            buf.guess_segment_properties()
            shape = hb.shape(font, buf, features)
            xOff, x, yOff, y = 0, 0, 0, 0
            Coco = CocoaPen(None)
    
    
            glyphname = []
            path = []
            for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
                gid = info.codepoint
                transformed = TransformPen(Coco, Offset(x + pos.x_offset, y + pos.y_offset))
                x += pos.x_advance
                y += pos.y_advance
                xOff += pos.x_offset
                yOff += pos.y_offset
            
                #Real Info Needed Here
                glyphname.append((
                font.get_glyph_name(gid), 
                xOff, x,
                yOff, y))
            
            # offset, width, height = None, None, None
     #        if direction in ('ltr', 'rtl'):
     #            offset = (0, -typo_descender)
     #            width  = x
     #            height = typo_ascender - typo_descender
     #        else:
     #            offset = (-vhea_descender, -y)
     #            width  = vhea_ascender - vhea_descender
     #            height = -y

            print(glyphname)
            return glyphname


text = stringProcess().texts
fontPath = stringProcess().font_path
ascend = stringProcess().typo_ascender
descend = stringProcess().typo_descender
feature = stringProcess().features

stringProcess().harfingz(text,fontPath,ascend,descend,feature)