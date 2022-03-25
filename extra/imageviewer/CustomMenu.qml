import QtQuick
import QtQuick.Controls

Menu {
 property int allowedx:parent.width
 property int actualx:x
 onCurrentIndexChanged : {
  for (var i=0;i<count;i++) {
   if (typeof itemAt(i).customsubmenu !== "undefined" && i!=currentIndex && itemAt(i).customsubmenu.opened && currentIndex>=0) {
   itemAt(i).arrow.requestPaint()
   itemAt(i).customsubmenu.close()
//   console.log('close menu.x,menu.y,itemAt.x,itemAt.y,itemAt.width,itemAt.height,allowedx,actualx,x',itemAt(i).menu.x,itemAt(i).menu.y,itemAt(i).x,itemAt(i).y,itemAt(i).width,itemAt(i).height,allowedx,actualx,x)
   } else if (typeof itemAt(i).customsubmenu !== "undefined" && i==currentIndex && !itemAt(i).customsubmenu.opened && currentIndex>=0) {
//   itemAt(i).customsubmenu.x=itemAt(i).x+itemAt(i).width
   itemAt(i).customsubmenu.allowedx=allowedx
    if (allowedx < actualx+itemAt(i).width+itemAt(i).customsubmenu.width) {
    itemAt(i).customsubmenu.x=-(itemAt(i).x+itemAt(i).width)
    itemAt(i).customsubmenu.actualx=actualx-(itemAt(i).x+itemAt(i).width)
    } else {
    itemAt(i).customsubmenu.x=itemAt(i).x+itemAt(i).width
    itemAt(i).customsubmenu.actualx=actualx+itemAt(i).x+itemAt(i).width
    }
//    console.log('open menu.x,menu.y,itemAt.x,itemAt.y,itemAt.width,itemAt.height,allowedx,actualx,x',itemAt(i).menu.x,itemAt(i).menu.y,itemAt(i).x,itemAt(i).y,itemAt(i).width,itemAt(i).height,allowedx,actualx,x)
   itemAt(i).customsubmenu.y=0
   itemAt(i).arrow.requestPaint()
   itemAt(i).customsubmenu.open()
   }
  }
 }
/* Component.onCompleted: {
 allowedx=parent.width
 actualx=x
 }*/
}
