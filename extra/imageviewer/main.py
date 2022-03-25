import os
from PySide6.QtQml import qmlRegisterType #, qmlRegisterUncreatableType
from PySide6.QtQuick import QQuickView
import re, sys
from PySide6.QtGui import QGuiApplication,QCursor,QSurfaceFormat
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Qt
from fileio import FileIO
from Rem import Re
from syntaxhighlighter import syntaxhighlighter

if __name__=='__main__':
 app=QGuiApplication()

 os.environ['XCURSOR_SIZE']='64'
 format=QSurfaceFormat()
 format.setSamples(4);
 QSurfaceFormat.setDefaultFormat(format);
# app.setOverrideCursor(QCursor("/home/minhinc/tmp/example/imageviewer/mycursor.png"))

 qmlfile=sys.argv[1] if len(sys.argv)>1 else re.sub(r'^(.*)[.]py$',r'\1',sys.argv[0])+'.qml'
 qmlRegisterType(FileIO, "FileIOPlugin", 1, 0, "FileIO")
 qmlRegisterType(syntaxhighlighter, "SyntaxHighlighter", 1, 0, "SyntaxHighlighter")
 reinstance=Re()
# if re.search(r'(?:\w+)?Window\s*{',open(qmlfile).read()):
 if re.search(r'^(?<!//)\s*(?:\w+)?Window\s*{\s*$',open(qmlfile).read(),flags=re.MULTILINE) and ( not re.search(r'/[*](?![*]/)*?\n\s*(?:\w+)?Window\s*{',open(qmlfile).read(),flags=re.DOTALL) or re.search(r'[*]/(?!/[*])*?\n\s*(?:\w+)?Window\s*{',open(qmlfile).read(),flags=re.DOTALL)):
  print('applicationwindow->',qmlfile)
  engine=QQmlApplicationEngine()
  engine.rootContext().setContextProperty("re",reinstance)
  engine.load(qmlfile)
 else:
  print('qquickitem->',qmlfile)
  engine=QQuickView()
  engine.setResizeMode(QQuickView.SizeRootObjectToView)
  engine.rootContext().setContextProperty("re",reinstance)
  engine.setSource(qmlfile)
  engine.show()
 res=app.exec()
 del engine
 sys.exit(res)
