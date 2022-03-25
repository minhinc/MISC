import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.platform
ApplicationWindow {
 id:itemid
 width:800;height:600
 visible:true
// flags:Qt.FramelessWindowHint
 Rectangle {
 anchors.fill:parent
 color:"#444444"
 }
 MouseArea {
 anchors.fill:parent
 acceptedButtons:Qt.RightButton
  onClicked: (mouse) => {
   if (mouse.button == Qt.RightButton) {
   contextmenuid.x=mouse.x
   contextmenuid.y=mouse.y
   contextmenuid.open()
   }
  }
 }
 SplitView {
 id:splitviewid
 anchors.fill:parent
  handle:Rectangle {
  implicitWidth:8
  color: SplitHandle.pressed ? "#81e889":(SplitHandle.hovered ? Qt.lighter("#c2f4c6",1.1):"#c2f4c6")
  }
  Keys.onPressed : function(event) {
  event.accepted = true
  keyleftright(event.key,event.modifiers,splitviewid.currentIndex)
  }
  function keyleftright(key,modifiers,index) {
   if (key == Qt.Key_Left || ((key == Qt.Key_Left) && (modifiers & Qt.ControlModifier))) {
    for (var i=0;i<splitviewid.itemAt(index).persistent.length;i++)
     if (splitviewid.itemAt(index).persistent[i][0]==splitviewid.itemAt(index).fileindex && splitviewid.itemAt(index).persistent[i][1]==false)
     splitviewid.itemAt(index).persistent[i][2].visible=false
  splitviewid.itemAt(index).fileindex=Math.max(splitviewid.itemAt(index).fileindex-1,0)
   for (var i=0;i<splitviewid.itemAt(index).persistent.length;i++)
    if (splitviewid.itemAt(index).persistent[i][0]==splitviewid.itemAt(index).fileindex && splitviewid.itemAt(index).persistent[i][1]==false)
    splitviewid.itemAt(index).persistent[i][2].visible=true
   } else if (key==Qt.Key_Right || ((key == Qt.Key_Right) && (modifiers & Qt.ControlModifier))) {
    for (var i=0;i<splitviewid.itemAt(index).persistent.length;i++)
     if (splitviewid.itemAt(index).persistent[i][0]==splitviewid.itemAt(index).fileindex && splitviewid.itemAt(index).persistent[i][1]==false)
     splitviewid.itemAt(index).persistent[i][2].visible=false
   splitviewid.itemAt(index).fileindex=Math.min(splitviewid.itemAt(index).fileindex+1,splitviewid.itemAt(index).files.length-1)
    for (var i=0;i<splitviewid.itemAt(index).persistent.length;i++)
     if (splitviewid.itemAt(index).persistent[i][0]==splitviewid.itemAt(index).fileindex && splitviewid.itemAt(index).persistent[i][1]==false)
     splitviewid.itemAt(index).persistent[i][2].visible=true
   }
  }
  onCurrentIndexChanged: {
   for (var i=0;i<count;i++)
   itemAt(i).focuschange(false)
  itemAt(currentIndex).focuschange(true)
  }
  function setfillwidth(index) {
   for (var i=0;i<splitviewid.count;i++) {
    splitviewid.itemAt(i).SplitView.preferredWidth=splitviewid.itemAt(i).width
    if (splitviewid.itemAt(i).SplitView.fillWidth==true)
    splitviewid.itemAt(i).SplitView.fillWidth=false
   }
  splitviewid.itemAt(index).SplitView.fillWidth=true
  }
 }
 MyMenu {
 id:contextmenuid
 }
 MyFileDialog {
 id:filedialogid
 }
}
