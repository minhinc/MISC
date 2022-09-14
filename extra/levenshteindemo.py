import re,os,sys
import sys;sys.path.append(os.path.expanduser(r'~')+r'/tmp/')
import kivy;kivy.require('2.1.0')
import kivy.uix.textinput
from kivy.lang import Builder
from kivy.graphics import Color,Rectangle
from kivy.app import App
from kivy.core.window import Window
import threading
import Levenshtein
from MISC.extra.debugwrite import print
from contextmenu import ContextMenu
import disablemultitouch

class LevenshteinDemo(kivy.uix.textinput.TextInput):
 TERMINATE='!TERM MRET!'
 def __init__(self,*arg,**kwarg):
  super(LevenshteinDemo,self).__init__(*arg,**kwarg)
  self.focus=True
  self.font_size=62
  self.contextmenu=ContextMenu(self,self.on_slot,mode='external')
  self.knnlist={}
  self.redwordlist=[]
  self.markedsentence=''
  self.englishdictionaryset=set(re.split(r'\s+',open(r'/usr/share/dict/british-english').read(),flags=re.DOTALL))
  self.threadingcondition=threading.Condition()
  Window.bind(on_request_close=self.on_close)
  self.backedlineslen=len(self._lines)
  self.t=threading.Thread(target=self.getneighbourlist)
  self.t.start()
 def getneighbourlist(self):
  print(f'><getneighbourlist')
  word=None
  levenshteindistancelist=[]
  _knnlist={}
  while True:
   while len(_knnlist)<len(self.knnlist):
    word=list(self.knnlist.keys())[len(_knnlist)]
#    print(f'<=>getneighbourlist word={word} len(self.knnlist)={len(self.knnlist)} knnlist={self.knnlist}')
    if word==self.TERMINATE:
     return
    levenshteindistancelist=[(i,Levenshtein.distance(word,i)) for i in self.englishdictionaryset]
    levenshteindistancelist.sort(key=lambda m:m[1])
    _knnlist[word]=[x[0] for x in levenshteindistancelist[:4]]
#   print(f'-- acquiring len(knnlist)={len(self.knnlist)} knnlist={self.knnlist}_knnlist={_knnlist}',flush=True)
   self.threadingcondition.acquire()
   print(f'<=>getneighbourlist wait',flush=True)
   for i in _knnlist:
    self.knnlist[i]=_knnlist[i][:]
   self.threadingcondition.wait()
#   print(f'--- wait broke _knnlist={_knnlist}')
   self.threadingcondition.release()
  print(r'<>getneighbourlist word={word} knn={self.knnlist[word]}')
#  return word
 def getbeginintersection(self,markedsentence,text):
  print(f'><getbeginintersection markedsentence={markedsentence} text={text}')
  maxi=min(len(markedsentence),len(text))
  mini=0
  while (maxi-mini)>1:
#   print(f'mini={mini} maxi={maxi}')
   if markedsentence[mini:mini+(maxi-mini)//2]==text[mini:mini+(maxi-mini)//2]:
    mini=mini+(maxi-mini)//2
   else:
    maxi=mini+(maxi-mini)//2
  return markedsentence[0:(mini+1 if maxi>mini and markedsentence[mini]==text[mini] else mini)]
 def on_text(self,instance,value):
  currentindex=0
  redwordlist=[]
  for i in re.split(r'\W+',self.text[currentindex:],flags=re.DOTALL):
   currentindex+=self.text[currentindex:].index(i)
   if not i.lower() in self.englishdictionaryset and not i in self.englishdictionaryset:
    redwordlist.append([currentindex,tuple([x-self.line_height if count==1 else x for count,x in enumerate(self._index2xy(currentindex))]),(self._get_text_width(i,self.tab_width,self._label_cached),self.line_height)])
    if i not in self.knnlist:
     self.threadingcondition.acquire()
     self.knnlist[i]=None
     self.threadingcondition.notify()
     self.threadingcondition.release()
   currentindex+=len(i)
  print(f'<=>on_text redwordlist={redwordlist}')
  self.canvas.after.clear()
  for i in redwordlist:
   self.canvas.after.add(Color(rgba=(1,0,0,0.30)))
   self.canvas.after.add(Rectangle(pos=i[1],size=i[2]))
 def on_slot(self,*arg):
  _indexword=None
  print(f'><on_slot arg={arg}')
  if arg[0]==self.contextmenu:
   _indexword=self._wordboundaryindex(self._xy2index(*self.contextmenu.button.pos))
   print(f'<=>on_slot contextmenu.button.pos={self.contextmenu.button.pos}')
   self.text=re.sub(r'^(.{'+str(_indexword[0][0])+r'}).{'+str(_indexword[0][1]-_indexword[0][0]+1)+r'}(.*)$',r'\1'+(arg[1] if not _indexword[1][0].isupper() else arg[1].title())+r'\2',self.text,flags=re.DOTALL)
   '''
   for count in [count for count in range(len(self.redwordlist)) if _indexword[0][0]==self.redwordlist[count][0]]:
    self.canvas.remove(Rectangle(pos=self.redwordlist[count][1],size=self.redwordlist[count][2]))
    del self.redwordlist[count]
   print(f'<=>on_slot count={count}')
   for i in self.redwordlist[count:]:
    i[0]+=len(arg[1])-len(_indexword[1])
   self.canvas.ask_update()
   '''
  self.focus=True
 def on_touch_down(self,touch):
  _indexword=None
  print(f'><on_touch_down touch.pos={touch.pos} self.redwordlist={self.redwordlist} index={self._xy2index(*touch.pos)} self.lineheight={self.line_height} self.knnlist={self.knnlist}')
  if (touch.button=='right'):
   _indexword=self._wordboundaryindex(self._xy2index(*touch.pos))
#   self.contextmenu.push(*self.redwordlist[[count for count in range(len(self.redwordlist)) if self.redwordlist[count][0]==_indexword[0][0]][0]][3])
   if _indexword[1] in self.knnlist and not self.knnlist[_indexword[1]]==None:
    self.contextmenu.push(*self.knnlist[_indexword[1]])
    self.contextmenu.open(touch.pos)
  self.focus=True
  return super(LevenshteinDemo,self).on_touch_down(touch)
 def _wordboundaryindex(self,index):
  print(f'><_wordboundaryindex index={index}')
  for i in range(index,-1,-1):
   if self.text[i] in [' ','\t','\n']:
    break
  i+=1 if self.text[i] in [' ','\t','\n'] else 0
  for j in range(index,len(self.text)):
   if self.text[j] in [' ','\t','\n','.',',','?','!']:
    break
  j-=1 if self.text[j] in [' ','\t','\n','.',',','?','!'] else 0
  print(f'<>_wordboundaryindex i,j={(i,j)} word={self.text[i:j+1]}')
  return ((i,j),self.text[i:j+1])
 '''
 def _wordsizexy(self,index):
  col,row=self.get_cursor_from_index(index)
  return self._get_text_width(self._wordboundaryindex(index)[1],self.tab_width,self._label_cached)
 '''
 def _xy2index2(self,x,y):
  col,row=self.get_cursor_from_xy(x,y)
  print(f'><_xy2index self.cursor_row={self.cursor_row} row,col={(row,col)} self.text={repr(self.text)} self._lines={self._lines} self.flags={self._lines_flags}')
  index=0
  lines = self._lines
  if not lines or len(lines)==1 and not lines[0] or row>=len(lines):
   return 0
  flags = self._lines_flags
#            index, cursor_row = cursor
  for _, line, flag in zip(range(min(row,len(lines))),lines,flags ):
   index += len(line)
   if flag & kivy.uix.textinput.FL_IS_LINEBREAK:
    index += 1
  if flags[row] & kivy.uix.textinput.FL_IS_LINEBREAK:
   index += 1
  index+=min(len(self._lines[row]),col)
  return index
 def _xy2index(self,x,y):
  col,row=self.get_cursor_from_xy(x,y)
  print(f'<=>_xy2index x,y={(x,y)} row,col={(row,col)}')
  index=0
  for count in range(min(row,len(self._lines))):
   index+=len(self._lines[count])
   if self.text[index]=='\n':
    index+=1
  index+=col
  return index
 def _index2xy(self,index):
  print(f'><_index2xy index={index} self.text={self.text}')
  def cursor_offset1(col,row):
   '''Get the cursor x offset on the current line.'''
   offset = 0
#      row = int(self.cursor_row)
#      col = int(self.cursor_col)
   lines = self._lines
   if col and row < len(lines):
    offset = self._get_text_width(
        lines[row][:col],
        self.tab_width,
        self._label_cached
    )
   return offset
  # return the current cursor x/y from the row/col
#  col,row=self.get_cursor_from_index(index)
  _index=len(re.sub('\n','',self.text[:index]))
  for i in range(len(self._lines)):
   if _index<(len(self._lines[i])-1):
    break
   _index-=len(self._lines[i])
  col,row=_index,i
  dy = self.line_height + self.line_spacing
  padding_left = self.padding[0]
  padding_top = self.padding[1]
  padding_right = self.padding[2]
  left = self.x + padding_left
  top = self.top - padding_top
  y = top + self.scroll_y
#      y -= self.cursor_row * dy
  y -= row * dy
  # Horizontal alignment
  halign = self.halign
  viewport_width = self.width - padding_left - padding_right
#      cursor_offset = self.cursor_offset()
  cursor_offset = cursor_offset1(col,row)
  base_dir = self.base_direction or self._resolved_base_dir
  auto_halign_r = halign == 'auto' and base_dir and 'rtl' in base_dir
  if halign == 'center':
#   row_width = self._get_row_width(self.cursor_row)
   row_width = self._get_row_width(row)
   x = (
       left
       + max(0, (viewport_width - row_width) // 2)
       + cursor_offset
       - self.scroll_x
   )
  elif halign == 'right' or auto_halign_r:
#   row_width = self._get_row_width(self.cursor_row)
   row_width = self._get_row_width(row)
   x = (
       left
       + max(0, viewport_width - row_width)
       + cursor_offset
       - self.scroll_x
   )
  else:
   x = left + cursor_offset - self.scroll_x
  print(f'<>_index2xy x,y={(x,y)}')
  return x, y

 def on_close(self,*arg):
  print(f'><on_close')
  self.threadingcondition.acquire()
  self.knnlist[self.TERMINATE]=None
  self.threadingcondition.notify()
  self.threadingcondition.release()
  self.t.join()
  App.get_running_app().stop()
  print(f'<>on_close')

class LevenshteinDemoApp(App):
 def build(self):
#  return Builder.load_string(kvstring)
  return LevenshteinDemo()

LevenshteinDemoApp().run() if __name__=='__main__' else None
