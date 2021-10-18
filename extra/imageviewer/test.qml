import QtQuick 2.0
import FileIOPlugin
TextEdit {
anchors.fill:parent
font.pointSize: textid.fontInfo.pointSize
color:"#ff0000"
 Text {
 id:textid
 text:"Hello World"
 color:"#00ff00"
 anchors.fill:parent
 minimumPixelSize: 10
 font.pixelSize:172
 fontSizeMode: Text.Fit
 visible:!parent.text && !parent.activeFocus
 }
 onTextChanged: {
 //font.pointSize=textid.fontInfo.pointSize
 textid.text=Qt.binding(function() {return text;})
 console.log('textid.text',textid.fontInfo.pointSize)
 }
 property var fileio:FileIO {
 source:'fileio.py'
 }
}
