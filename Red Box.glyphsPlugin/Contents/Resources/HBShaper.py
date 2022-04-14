from fontTools.ttLib import TTFont
import uharfbuzz as hb
import io

Binary = "/Users/fadhlschriftlabor/Documents/NotoSansKhmer-Regular.otf"
# Binary01 = "/Users/fadhlschriftlabor/Documents/NotoSansMyanmar-Regular.otf"
letters = "ꦏ អក្សរខ្មែរ"
# letters01 = "က္ခ"

class GlyphInfo:

    def __init__(self, gid, glyphname, xAd, yAd, xOff, yOff):
        self.gid = gid
        self.glyphname = glyphname
        self.xAd = xAd
        self.yAd = yAd
        self.xOff = xOff
        self.yOff = yOff


    def __repr__(self):
        return "GlyphInfo(gid={}, glyphname={}, xAd={}, yAd={}, xOff={}, yOff={})".format(self.gid, self.glyphname, self.xAd, self.yAd, self.xOff, self.yOff)

class HBShaping:
    
    @classmethod
    def fromPath(cls, path):
        with open(path, "rb") as f:
            fontData = f.read()
        return cls(fontData)

    def __init__(self, fontData, ttFont=None):
        self.fontData = fontData

        self.face = hb.Face(self.fontData)
        self.font = hb.Font(self.face)
        if ttFont is None:
            f = io.BytesIO(self.fontData)
            ttFont = TTFont(f, lazy=True)
        self._ttFont = ttFont

        self.glyphOrder = ttFont.getGlyphOrder()
        #self.features = self.getFeatures(self._ttFont)

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
    
    def shape(self, text, features=None, direction=None):
        if features is None:
            features = {}
        
        buf = hb.Buffer()
        buf.add_str(text) 

        if direction is not None:
            buf.direction(direction)

        buf.guess_segment_properties()
        buf.cluster_level = hb.BufferClusterLevel.MONOTONE_CHARACTERS

        #msgfunc = self.buildMessageHistoryFunction(buf)
        #buf.set_message_func(msgfunc)

        hb.shape(self.font, buf)

        # glyphOrder = self.glyphOrder
        infos = []

        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            #infos.append((info.codepoint, glyphOrder[info.codepoint], info.cluster, *pos.position))
            glyphName = self.font.get_glyph_name(info.codepoint)
            xAdv = pos.x_advance
            yAdv = pos.y_advance
            xOff = pos.x_offset
            yOff = pos.y_offset

            infos.append(GlyphInfo(info.codepoint, glyphName, xAdv, yAdv, xOff, yOff))
        
        return infos 

s = HBShaping.fromPath(Binary)
print(s.shape(letters))