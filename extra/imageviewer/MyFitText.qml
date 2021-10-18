import QtQuick 2.0
import QtQuick.Controls
Rectangle {
color:"#fff"
property alias text:textid.text
 TextEdit {
 color:"#440000"
 anchors.fill:parent
  Text {
  id:textid
  text:"Milli Second"
  color:"#ffaa00"
  anchors.fill:parent
  anchors.rightMargin:20
  minimumPixelSize: 10
  font.pixelSize:172
  fontSizeMode: Text.Fit
  visible:!parent.text && !parent.activeFocus
  }
  onTextChanged: {
  textid.text=text
  font.pointSize=textid.fontInfo.pointSize
  }
 }
}
