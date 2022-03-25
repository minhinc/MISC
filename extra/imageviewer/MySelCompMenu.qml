import QtQuick
import QtQuick.Controls

Menu {
 Menu {
 id:menucolorid 
 title:"&TextColor"
  MenuItem {
  id:menuitemgreenid
  text:"green"
  onTriggered : textcolor="green"
  }
  MenuItem {
  id:menuitemredid
  text:"red"
  onTriggered : textcolor="red"
  }
  MenuItem {
  id:menuitemwhiteid
  text:"white"
  onTriggered : textcolor="white"
  }
  MenuItem {
  id:menuitemblueid
  text:"blue"
  onTriggered : textcolor="blue"
  }
 }
 MenuItem {
 id:arrowid
 text:qsTr("arrow")
  onTriggered: {
  texteditid.visible=true
  selComp.mode=Const.Menu.Arrow
  selComp.textcolor="#ffff00"
  selComp.bordercolor="black"
//  selComp.color="black"
  if (selComp.friendnode==undefined)
  selComp.friendnode=triangleComponent.createObject(selComp,{friendobj:selComp})
  else
  selComp.friendnode.visible=true
  }
 }
 MenuItem {
 id:hollowid
 text:qsTr("hollow")
  onTriggered: {
  texteditid.visible=false
  selComp.mode=Const.Menu.Hollow
  selComp.border.width=2
  selComp.friendnode.visible=false
  selComp.rotation=0
  selComp.color="#00000000"
  }
 }
 MenuItem {
 id:persistentid
 text:qsTr("persistent")
  onTriggered: {
   for (var i=0;i<selComp.parent.persistent.length;i++) {
    if (selComp.parent.persistent[i][2]==selComp) {
    selComp.parent.persistent[i][1]=!selComp.parent.persistent[i][1]
    selComp.border.color=(selComp.parent.persistent[i][1]==false?'steelblue':'steelblue')
//     if (selComp.parent.fileindex!=i && selComp.parent.persistent[i][1]==false)
     if (selComp.parent.fileindex!=selComp.parent.persistent[i][0] && selComp.parent.persistent[i][1]==false)
     selComp.visible=false
    }
   }
  }
 }
 Menu {
 id:menubackcolorid 
 title:"&BackColor"
  MenuItem {
  id:backcolorgreenid
  text:"green"
  onTriggered : selComp.color="green"
  }
  MenuItem {
  id:backcolorredid
  text:"red"
  onTriggered : selComp.color="red"
  }
  MenuItem {
  id:backcolorwhiteid
  text:"white"
  onTriggered : selComp.color="white"
  }
  MenuItem {
  id:backcolorblueid
  text:"blue"
  onTriggered : selComp.color="blue"
  }
 }
}
