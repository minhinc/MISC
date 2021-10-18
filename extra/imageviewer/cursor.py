import sys
from PySide6.QtCore import *    
from PySide6.QtGui import *
from PySide6.QtDeclarative import *



class CursorArea (QDeclarativeItem):

    def __init__(self, parent = None):
        QDeclarativeItem.__init__(self, parent)
        self._cursors = Qt.CursorShape.ArrowCursor
        self._cursorsPix = "None"
        self._cursorsPixUrl = []

        self.dictPix = {"lapizAzul": QCursor(QPixmap("lapiz1.png"),1,32),
                        "lapizVerde": QCursor(QPixmap("lapiz1.png"),1,32),
                        "lapizCorona": QCursor(QPixmap("lapiz1.png"),1,32),
                        }


    def getCursors(self):
        return self_cursors

    def setCursors(self,value):
        self._cursors = value
        self.setCursor(value)
    cursors = Property(Qt.CursorShape, getCursors, setCursors)

    def getCursorsPix(self):
        return self._cursorsPix

    def setCursorsPix(self, value):
        print (value)
        pixmap = self.buscarPixmap(value)
        self.setCursor(pixmap)
    cursorsPix = Property("QString", getCursorsPix, setCursorsPix)

    def buscarPixmap(self, pix):
        if (pix in self.dictPix) == True:
            pixmap = self.dictPix[pix]
        else:
            pixmap = Qt.CursorShape.WhatsThisCursor
        return pixmap

    def getCursorsPixUrl(self):
        return self._cursorsPixUrl

    def setCursorsPixUrl(self, lista):
        print (lista)

        self.setCursor(QCursor(QPixmap(lista[0]),lista[1],lista[2]))
    cursorsPixUrl = Property("QVariantList", getCursorsPixUrl, setCursorsPixUrl)

