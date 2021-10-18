import QtQuick
import QtQuick.Controls

Item {
id:itemid
property alias text: textid.text
property alias buttonid:buttonid
 ScrollView {
 id:scrollviewid
 anchors.top:parent.top
 width:parent.width
 height:parent.height-buttonid.height
// background:Rectangle { color:"#aaaa88" }
 background:Rectangle { color:"black" }
 ScrollBar.horizontal.policy:ScrollBar.AlwaysOff
  ScrollBar.vertical.contentItem : Rectangle {
  implicitWidth:6
  implicitHeight:20
  color:scrollviewid.pressed ? "orange":"green"
  }
  function scrolltobottom() { ScrollBar.vertical.position=1.0-ScrollBar.vertical.size;  }
  Text {
  id:textid
  width:itemid.width-50
  height:parent.height
  color:"white"
  wrapMode:Text.Wrap
  text:""
   onTextChanged: scrollviewid.scrolltobottom()
  }
 }
 Button {
 id:buttonid
 anchors.bottom:parent.bottom
 anchors.horizontalCenter:parent.horizontalCenter
 text:"Ok"
 }
}
