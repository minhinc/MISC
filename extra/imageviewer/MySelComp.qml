import QtQuick
import QtQuick.Controls

Rectangle {
id: selComp
property alias textcolor:texteditid.color
property alias borderwidth:selComp.border.width
property alias bordercolor:selComp.border.color
//property alias backcolor:selComp.color
property real fractionX:0.0
property real fractionY:0.0
//property int rotationangle:0
property var friendnode:undefined
property int mode:Const.None
transformOrigin:Item.Center
 border { width: 2;color: "steelblue";}
 signal entered()
 signal exited()
color: "#354682B4"
width:parent.paintedWidth/Const.width;height:parent.paintedWidth/Const.height
property int rulersSize: 18
 onXChanged: {
  if (parent.paintedWidth!=0)
   x=parent.getfractionX(Math.min(x,parent.width-width),width);
 }
 onYChanged: {
  if (parent.paintedHeight!=0)
   y=parent.getfractionY(Math.min(y,parent.height-height),height);
 }
 Keys.onPressed : function(event) {
  if (event.key == Qt.Key_R) {
   if (event.modifiers & Qt.ShiftModifier)
    rotation=(rotation+5)%360
   else
    rotation=(rotation-5)%350
  } else if (event.key == Qt.Key_Left && !(event.modifiers & Qt.ControlModifier)) {
   selComp.x=Math.max(selComp.x-10,0)
   event.accepted=true
  } else if (event.key == Qt.Key_Right && !(event.modifiers & Qt.ControlModifier)) {
   selComp.x=Math.min(selComp.x+10,selComp.parent.width)
   event.accepted=true
  } else if (event.key == Qt.Key_Down && !(event.modifiers & Qt.ControlModifier)) {
   selComp.y=Math.min(selComp.y+10,selComp.parent.height)
   event.accepted=true
  } else if (event.key == Qt.Key_Up && !(event.modifiers & Qt.ControlModifier)) {
   selComp.y=Math.max(selComp.y-10,0)
   event.accepted=true
  } else if (event.key == Qt.Key_Tab){
   parent.tabchanged(selComp);
  }
 }
 MouseArea {     // drag mouse area
 anchors.fill: parent
 acceptedButtons:Qt.LeftButton | Qt.RightButton
  drag{
  target: parent
  minimumX: 0
  minimumY: 0
  maximumX: parent.parent.width - parent.width
  maximumY: parent.parent.height - parent.height
  smoothed: true
  filterChildren:true
  }
  onClicked: (mouse)=> {
//  parent.forceActiveFocus()
   selComp.forceActiveFocus()
   if (mouse.button == Qt.RightButton) {
   menuid.x=mouse.x
   menuid.y=mouse.y
   menuid.open()
   }
  }
  onDoubleClicked: {
  parent.parent.destroying(selComp)
  parent.destroy()        // destroy component
  }
  hoverEnabled:true
  onEntered: parent.entered();
  onExited: parent.exited();
  TextEdit {
  id:texteditid
  width:parent.width*0.80;height:parent.height*0.80
  anchors.centerIn:parent
  color:"#ffffff"
  font.pointSize:textid.fontInfo.pointSize
   Text {
   id:textid
   anchors.fill:parent
   anchors.bottomMargin:selComp.borderwidth/2
   text:"Click Here"
   color:"#ffff00"
   minimumPixelSize:2
   font.pixelSize:172
   fontSizeMode:Text.Fit
   visible:!parent.text && !parent.activeFocus
   }
   onTextChanged: {
   textid.text=Qt.binding(function() { return text;})
   }
   MouseArea {
   anchors.fill:parent
   propagateComposedEvents:true
   acceptedButtons:Qt.LeftButton | Qt.RightButton
 //  preventStealing:true
    onClicked: (mouse)=> {
     if (mouse.button == Qt.LeftButton) {
     texteditid.forceActiveFocus()
     texteditid.cursorPosition=texteditid.positionAt(mouse.x,mouse.y)
     mouse.accepted=true
     }
    }
    onDoubleClicked: {
     selComp.parent.destroying(selComp)
     selComp.destroy()
    }
   }
  }
 }
 Component {
 id:triangleComponent
  MyLine {
  }
 }
// function createarrow() {
//   friendnode=triangleComponent.createObject(selComp,{friendobj:selComp})
// }

 Rectangle {
 id:leftrect
 width: rulersSize; height: rulersSize; radius: rulersSize; color: "steelblue";
 anchors.horizontalCenter: parent.left
 anchors.verticalCenter: parent.verticalCenter
  visible:false
  MouseArea {
  anchors.fill: parent
   drag{ target: parent; axis: Drag.XAxis }
   onMouseXChanged: {
    if(drag.active){
    let fraction=(selComp.width - mouseX)/selComp.parent.paintedWidth;
    selComp.width = Qt.binding(function() { return selComp.parent.paintedWidth * fraction});
    selComp.x = selComp.x + mouseX
     if(selComp.width < 30) {
     let fraction=30/selComp.parent.paintedWidth
     selComp.width = Qt.binding(function() { return selComp.parent.paintedWidth * fraction});
     }
    }
   }
  }
  Connections {
  target:selComp
   function onEntered() { leftrect.visible=(selComp.mode==Const.Menu.Arrow?false:true) }
//   function onExited() { leftrect.visible=(selComp.mode==Const.Menu.Arrow?true:false); }
   function onExited() { leftrect.visible=false; }
  }
 }

 Rectangle {
 id:rightrect
 width: rulersSize; height: rulersSize; radius: rulersSize; color: "steelblue";
 anchors.horizontalCenter: parent.right
 anchors.verticalCenter: parent.verticalCenter
  visible:false
  MouseArea {
  anchors.fill: parent
   drag{ target: parent; axis: Drag.XAxis }
   onMouseXChanged: {
    if(drag.active){
    let fraction=(selComp.width+mouseX)/selComp.parent.paintedWidth;
    selComp.width = Qt.binding(function() { return selComp.parent.paintedWidth * fraction;})
     if(selComp.width < 50) {
     let fraction=50/selComp.parent.paintedWidth
     selComp.width=Qt.binding(function() { return selComp.parent.paintedWidth * fraction })
     }
    }
   }
  }
  Connections {
  target:selComp
   function onEntered() { rightrect.visible=true;}
   function onExited() { rightrect.visible=false; }
  }
 }

 Rectangle {
 id:toprect
 width: rulersSize;height: rulersSize;radius: rulersSize
 color: "steelblue"
 anchors.horizontalCenter: parent.horizontalCenter
 anchors.verticalCenter: parent.top
  MouseArea {
  anchors.fill: parent
   drag{ target: parent; axis: Drag.YAxis }
   onMouseYChanged: {
    if(drag.active){
    let fraction=(selComp.height - mouseY)/selComp.parent.paintedWidth
     selComp.height=Qt.binding(function() { return selComp.parent.paintedWidth * fraction; })
    selComp.y = selComp.y + mouseY
     if(selComp.height < 20) {
     let fraction=20/selComp.parent.paintedWidth
      selComp.height=Qt.binding(function() { return selComp.parent.paintedWidth * fraction;})
     }
    }
   }
  }
  Connections {
  target:selComp
   function onEntered() { toprect.visible=true;}
   function onExited() { toprect.visible=false;}
  }
 }

 Rectangle {
 id:bottomrect
 width: rulersSize;height: rulersSize;radius: rulersSize
 color: "steelblue"
 anchors.horizontalCenter: parent.horizontalCenter
 anchors.verticalCenter: parent.bottom
  MouseArea {
  anchors.fill: parent
   drag{ target: parent; axis: Drag.YAxis }
   onMouseYChanged: {
    if(drag.active){
    let fraction=(selComp.height + mouseY)/selComp.parent.paintedWidth
     selComp.height=Qt.binding(function() { return selComp.parent.paintedWidth * fraction;})
     if(selComp.height < 20) {
     let fraction=20/selComp.parent.paintedWidth
      selComp.height=Qt.binding(function() { return selComp.parent.paintedWidth * fraction;})
     }
    }
   }
  }
  Connections {
  target:selComp
   function onEntered() { bottomrect.visible=true;}
   function onExited() { bottomrect.visible=false;}
  }
 }
 MySelCompMenu {
 id:menuid
 }
// Component.onCompleted : selComp.forceActiveFocus()
}
