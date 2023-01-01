import QtQuick
import QtQuick.Controls
import FileIOPlugin
AnimatedImage {
 property int currentindex:0
 property var files:undefined
 property int fileindex:-1
// fillMode:Image.PreserveAspectFit
 fillMode:splitviewid.itemAt(currentindex).width<sourceSize.width?Image.PreserveAspectFit:Image.Pad
 property real fractionX:0.0
 property real fractionY:0.0
 property var persistent:[]
 MouseArea {
 anchors.fill:parent
 acceptedButtons:Qt.LeftButton | Qt.RightButton
 propagateComposedEvents:true
  onClicked: function(mouse) {
   splitviewid.setCurrentIndex(parent.currentindex)
   timerid.interval=parseInt(texteditid.text);texteditid.visible=false;labelid.visible=true
  if (mouse.button==Qt.LeftButton) {
   splitviewid.setfillwidth(parent.currentindex)
   parent.forceActiveFocus()
//  } else if (mouse.button==Qt.RightButton && !re.search('^animation',contextmenuid.items[contextmenuid.items.length-1].text,re.I)) {
  } else if (mouse.button==Qt.RightButton && !re.search('^animation',contextmenuid.itemAt(contextmenuid.count-1).text,re.I)) {
   contextmenuid.addEntry('animation...')
//   contextmenuid.items[contextmenuid.items.length-1].triggered.connect(function() {if (timerid.running) {timerid.stop();} else {timerid.restart();}})
   contextmenuid.itemAt(contextmenuid.count-1).triggered.connect(function() {if (timerid.running) {timerid.stop();} else {timerid.restart();}})
  }
   mouse.accepted=false
  }
  onDoubleClicked: function(mouse) {
   let fraction1=(Math.max(0,Math.min(parent.paintedWidth-parent.paintedWidth/Const.width,mouse.x-parent.paintedWidth/(Const.width*2))))/parent.paintedWidth
   let fraction2=(Math.max(0,Math.min(parent.paintedHeight-parent.paintedHeight/Const.height,mouse.y-parent.paintedHeight/(Const.height*2))))/parent.paintedHeight
//   persistent.push([fileindex,false,selectionComponent.createObject(parent,{x=Qt.binding(function() {return parent.paintedWidth*fraction1;}),y=Qt.binding(function() {return parent.paintedHeight*fraction2;})})])
   persistent.push([fileindex,false,selectionComponent.createObject(parent,{x:paintedWidth*fraction1,y:paintedHeight*fraction2})])
  }
 }
 Keys.onPressed : function(event) {
  var activefocusfound=false;
  if ((event.modifiers & Qt.ControlModifier) && (event.modifiers & Qt.AltModifier))
   fillMode=(fillMode==Image.PreserveAspectFit?Image.Pad:Image.PreserveAspectFit)
  else if (event.key==Qt.Key_Tab) {
   for (var i=0;i<persistent.length;i++)
    if ((persistent[i][0]==fileindex || persistent[i][1]==true) && persistent[i][2].activeFocus==true)
     activefocusfound=true
   if (activefocusfound==false)
    persistent[0][2].forceActiveFocus();
  }
 }
 Label {
 id:labelid
 anchors {top:parent.top;right:parent.right;rightMargin:parent.width/60;topMargin:parent.width/60}
 color:"#aaaaaa"
 font.pixelSize:parent.width/80
 text:re.sub('^.*/','',String(parent.files[parent.fileindex]))
  MouseArea {
  anchors.fill:parent
   onDoubleClicked: { 
   texteditid.visible=true 
   labelid.visible=false
   }
  }
 }
 MyFitText {
 id:texteditid
 width:labelid.width*2;height:labelid.height
 anchors.centerIn:labelid
 text:"1000"
 visible:false
 }
 function getfractionX(x,widthpar) {
  let fraction
  if (x < (width-paintedWidth)/2 || (x+widthpar) > (width+paintedWidth)/2) {
  fraction=x/(width==0?width+1:width)
  fractionX=(parent.width==0?fractionX:fraction)
  fraction=fractionX
  return Qt.binding(function() { return width*fraction;})
  } else {
  fraction=(x-(width-paintedWidth)/2)/(paintedWidth==0?paintedWidth+1:paintedWidth)
  fractionX=(fraction==0?fractionX:fraction)
  fraction=fractionX
  return Qt.binding(function() { return (width-paintedWidth)/2+paintedWidth*fraction;})
  }
 }
 function getfractionY(y,heightpar) {
  let fraction
  if (y < (height-paintedHeight)/2 || (y+heightpar) > (height+paintedHeight)/2) {
  fraction=y/(height==0?height+1:height)
  fractionY=(parent.height==0?fractionY:fraction)
  fraction=fractionY
  return Qt.binding(function() { return height*fraction;})
  } else {
  fraction=(y-(height-paintedHeight)/2)/(paintedHeight==0?paintedHeight+1:paintedHeight)
  fractionY=(y!=0 && fraction==0?fractionY:fraction)
  fraction=fractionY
  return Qt.binding(function() { return (height-paintedHeight)/2+paintedHeight*fraction;})
  }
 }

 onFileindexChanged: {
  if (fileindex>=0) {
   source=files[fileindex]
   if (fileindex==0 || fileindex==files.length-1)
    timerid.stop()
  } else
   source='file://'+fileioid.cachefile(re.sub('^file://','',files[0],re.I))
 }
 Component {
 id: selectionComponent
  MySelComp {
  }
 }
 Timer {
 id:timerid
 interval:1000; running:false; repeat:true
 onTriggered: splitviewid.keyleftright(Qt.Key_Right,Qt.NoModifier,currentindex)
 }
 function focuschange(focusin) {
  if (focusin==true)
   forceActiveFocus()
  else {
  focus=false
//   if (re.search('^animation',contextmenuid.items[contextmenuid.items.length-1].text,re.I))
   if (re.search('^animation',contextmenuid.itemAt(contextmenuid.count-1).text,re.I))
//   contextmenuid.removeItem(contextmenuid.items[contextmenuid.items.length-1])
   contextmenuid.removeItem(contextmenuid.itemAt(contextmenuid.count-1))
  }
 }
 FileIO {
 id:fileioid
 }
 function tabchanged(selfcompp) {
//  console.log('tabchanged',persistent)
  for (var i=0;i<persistent.length;i++) {
   if (selfcompp==persistent[i][2]) {
    if (persistent[(i+1)%persistent.length][0]!=fileindex && persistent[(i+1)%persistent.length][1]==false) {
     for (var j=(i+1)%persistent.length;j!=i;j=(j+1)%persistent.length) {
      if (persistent[j][0]==fileindex || persistent[j][1]==true) {
       persistent[j][2].forceActiveFocus()
       break;
      }
     }
    } else 
     persistent[(i+1)%persistent.length][2].forceActiveFocus()
    break
   }
  }
 }
 function destroying(selfcompp) {
  var j=0;
  for (var i=0;i<persistent.length;i++) {
   if (selfcompp!=persistent[i][2] && (persistent[i][0]==fileindex || persistent[i][1]==true))
    persistent[i][2].forceActiveFocus()
   else if (selfcompp==persistent[i][2] && (persistent[i][0]==fileindex || persistent[i][1]==true))
    j=i
  }
  persistent.splice(j,1)
 }
}
