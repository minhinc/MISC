import QtQuick
import QtQuick.Controls

MenuItem {
id:buttonid
text:qsTr("custommenuitem..")
property var customsubmenu:undefined
 arrow:Canvas {
 x:parent.width - width
 implicitWidth:19;implicitHeight:buttonid.height
 visible:customsubmenu==undefined?false:true
  onPaint: {
//  console.log('onPaint parent.width,parent.height,width,height,x,y',parent.width,parent.height,width,height,x,y)
  var ctx = getContext("2d")
  ctx.fillStyle = highlighted ? "#ffffff" : "#21be2b"
/*  ctx.moveTo(15,15)
  ctx.lineTo(width-15,height/2)
  ctx.lineTo(15,height-15)*/
  ctx.moveTo(0,height/3)
  ctx.lineTo(width/3,height/2)
  ctx.lineTo(0,height*2/3)
  ctx.closePath()
  ctx.fill()
  }
 }
 onClicked: (mouse)=> {
// console.log('Button clicked manuid.x,buttonid.menu.y,buttonid.menu.width,buttonid.menu.height,x,y',buttonid.menu.x,buttonid.menu.y,buttonid.menu.width,buttonid.menu.height,x,y)
 let pmenu=menu
  for (var i=0;i<pmenu.count; i++)
   if (pmenu.itemAt(i).customsubmenu != undefined && customsubmenu.opened)
    pmenu=pmenu.itemAt(i).customsubmenu
  while (pmenu.parent.menu != undefined && pmenu.parent.menu != pmenu) {
  pmenu.close()
  pmenu=pmenu.parent.menu
  }
 pmenu.close()
 /*if (typeof menu.parent.menu !=="undefined")
 menu.parent.menu.close()*/
 }
/* Connections {
 target:buttonid.menu
  function onCurrentIndexChanged() {
   if (buttonid.customsubmenu != undefined && !buttonid.customsubmenu.opened && buttonid.menu.itemAt(buttonid.menu.currentIndex)==buttonid) {
   console.log('submenu opening manuid.x,buttonid.menu.y,buttonid.menu.width,buttonid.menu.height,x,y',buttonid.menu.x,buttonid.menu.y,buttonid.menu.width,buttonid.menu.height,x,y)
   buttonid.customsubmenu.x=buttonid.width
   buttonid.customsubmenu.y=0
    buttonid.customsubmenu.open()
   } else if (buttonid.customsubmenu != undefined && buttonid.customsubmenu.opened && buttonid.menu.itemAt(buttonid.menu.currentIndex)!=buttonid) {
   buttonid.customsubmenu.close()
   console.log('submenu closed currentindex',menuid.currentIndex,this,this.parent,parent,buttonid)
   }
  }
 }*/
}
