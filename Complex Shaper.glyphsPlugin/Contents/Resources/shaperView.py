from GlyphsApp import *
from HBShaper import HBShaping
import vanilla, traceback
from AppKit import NSView, NSColor, NSBezierPath, NSWidth, NSHeight, NSAffineTransform, NSFrameRect, NSRect, NSMakePoint


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
            # print(self.wrapper._textWidth)

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