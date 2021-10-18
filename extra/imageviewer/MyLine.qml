import QtQuick
import QtQuick.Shapes
Rectangle {
id:rectid
property var friendobj:undefined
anchors.verticalCenter:friendobj.verticalCenter
anchors.right:friendobj.left
width:friendobj.width/4
height:friendobj.height*4/3
color:"#00000000"
/* transform: [
  Translate { x:-(friendobj.width+width)/2 },
//  Rotation { origin.x:width/2;origin.y:height/2;angle:friendobj.rotation},
  Rotation { origin.x:width/2;origin.y:height/2;angle:0},
  Translate { x:(friendobj.width+width)/2 }
 ]*/
 Shape {
 anchors.fill: parent
  ShapePath {
  strokeWidth: 4
  strokeColor: "red"
  fillColor:"transparent"
  startX: 0; startY: height/2
   PathLine { x: width; y: 0 }
   PathLine { x: width; y: height }
   PathLine { x: 0; y: height/2 }
  }
 }
}
