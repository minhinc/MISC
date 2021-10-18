import re
from PySide6.QtCore import Qt, Slot
import PySide6.QtCore
from PySide6.QtGui import QSyntaxHighlighter, QColor, QFont, QFontDatabase, QKeySequence, QTextCharFormat
from PySide6.QtQuick import QQuickTextDocument

class syntaxhighlighter(QSyntaxHighlighter) :
 def __init__(self,parent=None):
  super(syntaxhighlighter,self).__init__(parent)
  self.handlelist=[]
  self.next=tmpnode=None
  if type(self)==syntaxhighlighter:
   for i in "qml","py","ffmpeg":
    if tmpnode:
     tmpnode.next=eval(i+"()")
     tmpnode=tmpnode.next
    else:
     self.next=tmpnode=eval(i+"()")
  self._mappings = {}
# def handle(self,textdocument,highlight,filename):
#  if self.next:
#   self.next.setdocument(textdocument,highlight,filename)
#  else:
#   print('No matching syntax highlighter')

 def handle(self):
  next=self.next
  self.handlelist=[]
  while next:
#  while next and not next.handle(self.filename):
   if next.handle(self.filename):
    self.handlelist.append(next)
   next=next.next
#  next=self.next.handle(self.filename)
#  return next if next else self
  self.handlelist=self.handlelist or (self,)
  return self.handlelist
#  return handlelist if handlelist else (self,)
# def add_mapping(self, pattern, format):
#  self._mappings[pattern] = format
 def add_mapping(self, pattern, **format):
  _format=QTextCharFormat()
  for i in format:
   eval('_format.'+i+'('+repr(format[i])+')')
  self._mappings[pattern]=_format

 def highlightBlock(self, text):
#  for pattern, format in self._mappings.items():
#  for pattern, format in self.handle()._mappings.items():
  for pattern, format in [x for i in self.handlelist for x in i._mappings.items()]:
   for match in re.finditer(pattern, text):
    if (match.groups()):
     for i in range(len(match.groups())):
      start, end = match.span(i+1)
      self.setFormat(start, end - start, format)
    else:
     start,end=match.span()
     self.setFormat(start,end-start,format)

 @Slot(QQuickTextDocument,bool,str)
 def setdocument(self,textdocument,highlight,filename):
#  self.chain.setdocument(textdocument,highlight,filename)
  self.filename=filename
  self.setDocument(textdocument.textDocument() if highlight else None)
  self.handle()

class qml(syntaxhighlighter):
 def __init__(self,parent=None):
  super(qml,self).__init__(parent)
  self.add_mapping(r'\b(console|readonly|function|import)\b',setForeground=QColor('#442200'))
  self.add_mapping(r'^\s*(\w+)\s*{\s*$',setForeground=Qt.blue)
  self.add_mapping(r'^\s*(import).*$',setFontItalic=True,setForeground=QColor('#aa5500'))
  self.add_mapping(r'^\s*(readonly)?\s*(property).*',setForeground=Qt.blue,setFontItalic=True)
  self.add_mapping(r'^\s*(import).*$',setForeground=Qt.blue,setFontItalic=True)
  self.add_mapping(r'//.*$', setBackground=QColor('#77ff77'))
  self.add_mapping(r'["\'][^"\']+["\']',setForeground=QColor('#ff0000'))

# def setdocument(self,textdocument,highlight,filename):
#  if re.search(r'[.]qml$',filename,flags=re.I):
#   print('QML',highlight,filename)
#   self.setDocument(textdocument.textDocument() if highlight else None)
#  else:
#   self.handle(textdocument,highlight,filename)

 def handle(self,filename):
  return re.search(r'[.]qml$',filename,flags=re.I)

class py(syntaxhighlighter):
 def __init__(self,parent=None):
  super(py,self).__init__(parent)
  self.add_mapping(r'^\s*(@.*)$',setForeground=QColor('#000040'),setFontItalic=True)
  self.add_mapping(r'\b(print|False|await|else|import|pass|None|break|except|in|raise|True|class|finally|is|return|and|continue|for|lambda|try|as|def|from|nonlocal|while|assert|del|global|not|with|async|elif|if|or|yield)\b',setForeground=QColor('#442200'))
  self.add_mapping(r'^\s*(class)\s+\w+(?:\(.*)?:$',setFontWeight=QFont.Bold,setForeground=Qt.blue)
  self.add_mapping(r'^\s*(def)\s+\w+\s*\(.*\)\s*:\s*$',setFontItalic=True,setForeground=Qt.blue)
  self.add_mapping(r'^\s*(from)?.*(import)\s+.*$',setFontItalic=True,setForeground=QColor('#aa5500'))
  self.add_mapping(r'([\'][^\']+[\']|["][^"]+["])',setForeground=QColor('#ff0000'))
  self.add_mapping(r'(?:(?<![\'"]))(#.*)$', setBackground=QColor('#77ff77'))
#  self.add_mapping(r'["][^"]+["]',setForeground=QColor('#ff0000'))
#  self._editor = QPlainTextEdit()
#  self._editor.setFont(font)
#  self._highlighter.setDocument(self._editor.document())

# def setdocument(self,textdocument,highlight,filename):
#  if re.search(r'[.]py$',filename,flags=re.I):
#   print('PY',highlight,filename)
#   self.setDocument(textdocument.textDocument() if highlight else None)
#  else:
#   self.handle(textdocument,highlight,filename)

 def handle(self,filename):
  return re.search(r'[.]py$',filename,flags=re.I)

class ffmpeg(syntaxhighlighter):
 def __init__(self,parent=None):
  super(ffmpeg,self).__init__(parent)
  self.add_mapping(r'\$',setFontItalic=True,setBackground=QColor('#ff007f'))
  self.add_mapping(r'##.*?##',setFontItalic=True,setBackground=QColor('#ff007f'))
 def handle(self,filename):
  return re.search(r'/ffmpeg',filename,flags=re.I)
