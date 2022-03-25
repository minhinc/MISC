import QtQuick
import QtQuick.Controls
import QtQuick.Window
import FileIOPlugin
import SyntaxHighlighter

ScrollView {
//id:scrollviewid
property alias currentindex:textArea.currentindex
property alias files:textArea.files
property alias fileindex:textArea.fileindex
property alias persistent:textArea.persistent
 TextArea {
 id: textArea
 property int currentindex:0
 property var files:undefined
 property int fileindex:-1
 property int mousex:0
 property int mousey:0
 property var persistent:[]
 wrapMode: TextArea.Wrap
 font.family:"Consolas"
 font.pointSize:textid.fontInfo.pointSize
 leftPadding: 6
 topPadding: 6
  Text {
  id:textid
  anchors.fill:parent
  anchors.rightMargin:20
  minimumPixelSize:1
  font.pointSize:72
  fontSizeMode:Text.HorizontalFit
  visible:false
  }
  background: Rectangle {color:"#fff"}
  Rectangle {
  id:rectcolorid
  width:50;height:50
  anchors.left:parent.left
  anchors.leftMargin:(splitviewid.itemAt(parent.currentindex).width-width)/2
  anchors.top:parent.top
  anchors.topMargin:(splitviewid.itemAt(parent.currentindex).height-height)/2
  color:"red"
  visible:false
  opacity:0.0
   Behavior on opacity {
    PropertyAnimation {
    duration:100
    }
   }
  }
  Timer {
  id:timerid
  interval:100; running:false; repeat:false
   onTriggered: {
   rectcolorid.visible=false;rectcolorid.opacity=0.0
   }
  }
  
  function textfit() {
  wrapMode=TextArea.Wrap
  textid.fontSizeMode=Text.HorizontalFit
  font.pointSize=Qt.binding( function() { return textid.fontInfo.pointSize; })
  splitviewid.itemAt(textArea.currentindex).width-=0.1;splitviewid.itemAt(textArea.currentindex).width+=0.1
  rectcolorid.visible=true
  rectcolorid.opacity=1.0
  timerid.restart()
  }
  Keys.onPressed : function(event) {
   if ((event.modifiers & Qt.ControlModifier) && (event.modifiers & Qt.AltModifier)) {
    textfit()
   }
   if (((event.key == Qt.Key_Plus && (event.modifiers & Qt.ShiftModifier)) || (event.key == Qt.Key_Equal)) && (event.modifiers & Qt.ControlModifier)) {
   textArea.wrapMode=TextArea.NoWrap
   font.pointSize = font.pointSize + 1
   } else if (event.key == Qt.Key_Minus && (event.modifiers & Qt.ControlModifier))
   font.pointSize = font.pointSize - 1
   if ((event.key == Qt.Key_Right || event.key==Qt.Key_Left) && (event.modifiers & Qt.ControlModifier))
    splitviewid.Keys.pressed(event)
   if ((event.key == Qt.Key_W) && (event.modifiers & Qt.ControlModifier)) {
    if (textArea.wrapMode==TextArea.NoWrap) {
    textfit()
    textid.fontSizeMode=Text.Fit
    textid.width=Qt.binding(function() { return splitviewid.itemAt(textArea.currentindex).width;})
    textid.height=Qt.binding(function() { return splitviewid.itemAt(textArea.currentindex).height;})
    } else {
    textArea.wrapMode=TextArea.NoWrap
    textid.width=textArea.width
    textid.height=textArea.height
    splitviewid.itemAt(textArea.currentindex).width-=0.1;splitviewid.itemAt(textArea.currentindex).width+=0.1
    }
   }
   if ((event.key == Qt.Key_X) && (event.modifiers & Qt.ControlModifier)) {
   textArea.persistent[textArea.persistent.length-1][2].x=textArea.mousex;textArea.persistent[textArea.persistent.length-1][2].y=textArea.mousey
   }
  }
  Label {
  anchors {top:parent.top;right:parent.right;rightMargin:parent.width/40;topMargin:parent.width/40}
  color:"#ff4422"
  font.pixelSize:parent.width/40
  text:re.sub('^.*/','',String(parent.files[parent.fileindex]))
  }
  MouseArea {
  anchors.fill: parent
  acceptedButtons: Qt.LeftButton | Qt.RightButton
  propagateComposedEvents:true
  preventStealing: true
   onClicked: (mouse)=> {
   textArea.mousex=mouse.x;textArea.mousey=mouse.y
   splitviewid.setCurrentIndex(textArea.currentindex)
    if (mouse.button == Qt.LeftButton) {
    splitviewid.setfillwidth(parent.currentindex)
    textArea.forceActiveFocus()
    textArea.cursorPosition=textArea.positionAt(mouse.x,mouse.y)
    }
    if (mouse.button == Qt.RightButton) {
//     if (!re.search('^save',contextmenuid.items[contextmenuid.items.length-1].text,re.I)){
     if (!re.search('^save',contextmenuid.itemAt(contextmenuid.count-1).text,re.I)){
     contextmenuid.addEntry('syntaxhighlight...')
//     contextmenuid.items[contextmenuid.items.length-1].triggered.connect(function() {syntaxhighlighterid.highlight=!syntaxhighlighterid.highlight;syntaxhighlighterid.setdocument(textArea.textDocument,syntaxhighlighterid.highlight,files[fileindex])})
     contextmenuid.itemAt(contextmenuid.count-1).triggered.connect(function() {syntaxhighlighterid.highlight=!syntaxhighlighterid.highlight;syntaxhighlighterid.setdocument(textArea.textDocument,syntaxhighlighterid.highlight,files[fileindex])})
     contextmenuid.addEntry('save...')
//     contextmenuid.items[contextmenuid.items.length-1].triggered.connect(function() {fileioid.save(re.sub('^file://','',textArea.files[textArea.fileindex],re.I),textArea.text);checktofiredialogid.title="Do you want fire?";if (re.search('/ffmpeg.*?[.]py$',textArea.files[textArea.fileindex],re.I)) checktofiredialogid.open();})
     contextmenuid.itemAt(contextmenuid.count-1).triggered.connect(function() {fileioid.save(re.sub('^file://','',textArea.files[textArea.fileindex],re.I),textArea.text);checktofiredialogid.title="Do you want fire?";if (re.search('/ffmpeg.*?[.]py$',textArea.files[textArea.fileindex],re.I)) checktofiredialogid.open();})
     }
    }
   mouse.accepted=false
   }
   onDoubleClicked: function(mouse) {
   let fraction1=(Math.max(0,Math.min(parent.contentWidth-parent.contentWidth/Const.width,mouse.x-parent.contentWidth/(Const.width*2))))/parent.contentWidth
   let fraction2=(Math.max(0,Math.min(parent.contentHeight-parent.contentHeight/Const.height,mouse.y-parent.contentHeight/(Const.height*2))))/parent.contentHeight
   persistent.push([fileindex,false,selectionComponent.createObject(parent,{x:contentWidth*fraction1,y:contentHeight*fraction2,textcolor:"green"})])
   }
  }
  onTextChanged: {
  textid.text=Qt.binding(function() { return text;})
  splitviewid.itemAt(textArea.currentindex).width-=0.1;splitviewid.itemAt(textArea.currentindex).width+=0.1
  }
  Component.onCompleted : {
  syntaxhighlighterid.setdocument(textDocument,syntaxhighlighterid.highlight,files[fileindex])
  }
  Component {
  id:selectionComponent
   MySelComp {
   }
  }
  Component {
  id:triangleComponent
   MyLine {
   }
  }
  function getfractionX(x) {
  let fraction=x/(paintedWidth==0?paintedWidth+1:paintedWidth)
  return Qt.binding(function() { return paintedWidth*fraction;})
  }
  function getfractionY(y) {
  let fraction=y/(paintedHeight==0?paintedHeight+1:paintedHeight)
  return Qt.binding(function() { return paintedHeight*fraction;})
  }
  onFileindexChanged: {
   if (fileindex>=0) {
   textArea.text=fileioid.filestring(re.sub('^file://','',files[fileindex],re.I))
   syntaxhighlighterid.setdocument(textDocument,syntaxhighlighterid.highlight,files[fileindex])
   }
  }
  MyCheckToFireDialog {
  id:checktofiredialogid
  width:splitviewid.itemAt(textArea.currentindex).width/Const.width
  height:splitviewid.itemAt(textArea.currentindex).width/(0.5*Const.height)
  x:(splitviewid.itemAt(textArea.currentindex).width-checktofiredialogid.width)/2
  y:(splitviewid.itemAt(textArea.currentindex).height-checktofiredialogid.height)/2
   background: Rectangle {
   anchors.fill:parent
   color:"white"
   }
  title:"Do you want to fire?"
  text:re.sub('^file://','',textArea.files[textArea.fileindex],re.I)+"\nfile will be processed with python3 interpreter\nPress Ok to continue\nPress Cancel to discontinue"
   onAccepted: {
   filestatusid.createObject(splitviewid.itemAt(textArea.currentindex))
   fileioid.fire(re.sub('^file://','',textArea.files[textArea.fileindex],re.I))
   textArea.readOnly=true
   }
  }
  Component {
  id:filestatusid
   MyFileStatus {
   id:filestatus2id
   width:splitviewid.itemAt(textArea.currentindex).width/1.5
   height:splitviewid.itemAt(textArea.currentindex).width/2
   x:(splitviewid.itemAt(textArea.currentindex).width-width)/2
   y:(splitviewid.itemAt(textArea.currentindex).height-height)/2
    Connections {
    target:fileioid
     function onThreaddataChanged(textvar) {
     filestatus2id.text+=textvar
     }
    }
    Connections {
    target:buttonid
     function onClicked() {
     textArea.readOnly=false
     fileioid.stopthread=true
     filestatus2id.destroy()
     }
    }
   }
  }
 }
 FileIO {
 id:fileioid
/*  onThreaddataChanged: (textvar)=> {
//  console.log('souce changed')
  textArea.obj.text+=textvar
//  textArea.text=filestring()
  }*/
// Component.onCompleted: source='fileio.py'
 }
 SyntaxHighlighter {
  id:syntaxhighlighterid
  property bool highlight:true
 }
 function focuschange(focusin) {
  if (focusin==true) {
  textArea.forceActiveFocus()
  textArea.cursorPosition=0
  } else {
  textArea.focus=false
//   if (re.search('^save',contextmenuid.items[contextmenuid.items.length-1].text,re.I)) {
   if (re.search('^save',contextmenuid.itemAt(contextmenuid.count-1).text,re.I)) {
//   contextmenuid.removeItem(contextmenuid.items[contextmenuid.items.length-1])
   contextmenuid.removeItem(contextmenuid.itemAt(contextmenuid.count-1))
//   contextmenuid.removeItem(contextmenuid.items[contextmenuid.items.length-1])
   contextmenuid.removeItem(contextmenuid.itemAt(contextmenuid.count-1))
   }
  }
 }
}
