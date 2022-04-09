from fontTools.ttLib import TTFont
from fontTools.pens.cocoaPen import CocoaPen
import uharfbuzz as hb
import io

Binary = "/Users/fadhlschriftlabor/Documents/NotoSansKhmer-Regular.otf"
Binary01 = "/Users/fadhlschriftlabor/Documents/NotoSansMyanmar-Regular.otf"
letters = "អិ"
letters01 = "က္ခ"

class HBShaping:
    
    @classmethod
    def fromPath(cls, path):
        with open(path, "rb") as f:
            fontData = f.read()
        return cls(fontData)

    def __init__(self, fontData, ttFont=None):
        self.fontData = fontData

        self.face = hb.Face(fontData)
        self.font = hb.Font(self.face)
        if ttFont is None:
            f = io.BytesIO(self.fontData)
            ttFont = TTFont(f, lazy=True)
        self._ttFont = ttFont

        self.glyphOrder = ttFont.getGlyphOrder()
        self.features = self.getFeatures(self._ttFont)

    def getFeatures(self, ttFont):
        ttFont = self._ttFont
        gsub = ttFont['GSUB']
        gpos = ttFont['GPOS']
        
        features = []

        if gsub:
            features_records = gsub.table.FeatureList.FeatureRecord
            features_tags = [f.FeatureTag for f in features_records]
            lookup_ids = [f.Feature.LookupListIndex for f in features_records]
            feature = {}
            #create a dictionary with feature tags as keys and lookup ids as values
            for tag, lookup_id in zip(features_tags, lookup_ids):
                feature[tag] = lookup_id
            features.append(feature)
        
        if gpos:
            features_records = gpos.table.FeatureList.FeatureRecord
            features_tags = [f.FeatureTag for f in features_records]
            lookup_ids = [f.Feature.LookupListIndex for f in features_records]
            feature = {}
            #create a dictionary with feature tags as keys and lookup ids as values
            for tag, lookup_id in zip(features_tags, lookup_ids):
                feature[tag] = lookup_id
            features.append(feature)

        return features
        # print(self._ttFont["GPOS"].table.LookupList.Lookup)
        #return ttFont["GSUB"].table.LookupList.Lookup

    def getLookupId(self, ttFont):
        pass

    #code are taken from Simon Cozens' Font Goggles fork
    def buildMessageHistoryFunction(self, buf):
            lastmessage = []
            resultlist = []
            def handle_message(msg):
                nonlocal resultlist
                nonlocal lastmessage
                resultlist.append((msg, [g.codepoint for g in buf.glyph_infos]))
            #     if msg.startswith("start"):
            #         lastmessage = tuple([g.codepoint for g in buf.glyph_infos])
            #     if msg.startswith("end"):
            #         lookup = re.findall("(\d+)", msg)
            #         thismessage = tuple([g.codepoint for g in buf.glyph_infos])
            #         if lastmessage != thismessage:
            #             glyphlist = [self.glyphOrder[g.codepoint] for g in buf.glyph_infos]
            #             resultlist.append("After lookup %i: %s" % (int(lookup[0]), "|".join(glyphlist)))
            return handle_message, resultlist
    
    def shape(self, text):

        blob = hb.Blob.from_file_path(self.fontData)
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()

        msgfunc, history = self.buildMessageHistoryFunction(buf)
        buf.set_message_func(msgfunc)

        hb.shape(self.font, buf)

        glyphOrder = self.glyphOrder
        infos = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            infos.append((info.codepoint, glyphOrder[info.codepoint], info.cluster, *pos.position))
        print([self.font.get_glyph_name(g.codepoint) for g in buf.glyph_infos])
        #print(infos, history)
        return infos, history

        # gids_trace = [[g.codepoint for g in infos] for infos in infos_trace]
        # advances_trace = [[g.x_advance for g in pos] for pos in positions_trace if pos]
    def drawFromPath(self, gid):
        
        pen = CocoaPen(None)
        drawing = font.draw_glyph_with_pen(gid, pen)
        
        return drawing

fs = HBShaping.fromPath(Binary)
fea = fs.features
print(fea)
fs.shape(letters)

# fs01 = HBShaping.fromPath(Binary01)
# fs01.shape(letters01)